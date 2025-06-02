defmodule CustomerSupportPhoenixWeb.ChatLiveLive.Show do
  use CustomerSupportPhoenixWeb, :live_view

  alias CustomerSupportPhoenix.Chat
  alias CustomerSupportPhoenix.Chat.{ChatSession, ChatMessage}
  alias CustomerSupportPhoenix.AiClient

  @impl true
  def mount(%{"id" => id}, _session, socket) do
    session = Chat.get_chat_session_with_messages!(id)

    message_changeset = ChatMessage.changeset(%ChatMessage{}, %{})
    title_changeset = ChatSession.changeset(session, %{})

    {:ok,
     socket
     |> assign(:page_title, page_title(session.title))
     |> assign(:session, session)
     |> assign(:messages, session.messages)
     |> assign(:message_form, to_form(message_changeset))
     |> assign(:title_form, to_form(title_changeset))
     |> assign(:editing_title?, false)
     |> assign(:sending_message, false)
    }
  end

  @impl true
  def handle_event("validate_message", %{"chat_message" => params}, socket) do
    changeset =
      %ChatMessage{}
      |> ChatMessage.changeset(params)
      |> Map.put(:action, :validate)

    {:noreply, assign(socket, :message_form, to_form(changeset))}
  end

  @impl true
  def handle_event("send_message", %{"chat_message" => params}, socket) do
    session = socket.assigns.session

    case Chat.create_message(session, "user", params["message"]) do
      {:ok, user_message} ->
        messages = socket.assigns.messages ++ [user_message]

        new_message_changeset = ChatMessage.changeset(%ChatMessage{}, %{})
        socket =
          socket
          |> assign(:messages, messages)
          |> assign(:message_form, to_form(new_message_changeset))
          |> assign(:sending_message, true)
          |> scroll_chat_to_bottom()

        history_for_ai = Enum.map(messages, fn msg -> %{sender: msg.sender, message: msg.message} end)
        Task.Supervisor.start_child(CustomerSupportPhoenix.TaskSupervisor, fn ->
          send_to_ai_and_reply(self(), session.id, user_message, history_for_ai)
        end)

        {:noreply, socket}

      {:error, changeset} ->
        {:noreply, assign(socket, :message_form, to_form(changeset))}
    end
  end

  @impl true
  def handle_event("submit_feedback", %{"message-id" => message_id, "rating" => rating}, socket) do
    message_id_int = String.to_integer(message_id)
    messages = socket.assigns.messages
    ai_message = Enum.find(messages, fn m -> m.id == message_id_int && m.sender == "ai" end)

    if ai_message do
      case Chat.create_or_update_feedback(ai_message, %{rating: rating}) do
        {:ok, feedback} ->
          updated_messages = Enum.map(messages, fn
            %{id: ^message_id_int} = msg ->
              %{msg | feedback: %{feedback | chat_message: msg}}
            msg -> msg
          end)
          {:noreply, assign(socket, :messages, updated_messages)}
        {:error, reason} ->
           IO.inspect(reason, label: "Feedback error")
           {:noreply, put_flash(socket, :error, "Failed to save feedback: #{inspect(reason)}")}
      end
    else
      {:noreply, put_flash(socket, :error, "Could not find AI message to add feedback to.")}
    end
  end

  @impl true
  def handle_event("start_edit_title", _, socket) do
    title_changeset = ChatSession.changeset(socket.assigns.session, %{})
    {:noreply,
      socket
      |> assign(:editing_title?, true)
      |> assign(:title_form, to_form(title_changeset))
    }
  end

  @impl true
  def handle_event("cancel_edit_title", _, socket) do
    {:noreply, assign(socket, :editing_title?, false)}
  end

  @impl true
  def handle_event("validate_title", %{"chat_session" => params}, socket) do
    changeset =
      socket.assigns.session
      |> ChatSession.changeset(params)
      |> Map.put(:action, :validate)

    {:noreply, assign(socket, :title_form, to_form(changeset))}
  end

  @impl true
  def handle_event("save_title", %{"chat_session" => params}, socket) do
    session = socket.assigns.session

    case Chat.update_chat_session(session, params) do
      {:ok, updated_session} ->
        {:noreply,
          socket
          |> assign(:session, updated_session)
          |> assign(:editing_title?, false)
          |> assign(:page_title, page_title(updated_session.title))
          |> put_flash(:info, "Title updated successfully.")
        }
      {:error, changeset} ->
        {:noreply, assign(socket, :title_form, to_form(changeset))}
    end
  end

  @impl true
  def handle_info({:ai_response, {:ok, ai_message, title_update_result}}, socket) do
    socket =
      case title_update_result do
        {:ok, new_title} when not is_nil(new_title) ->
          assign(socket, page_title: page_title(new_title), session: %{socket.assigns.session | title: new_title})
        _ -> socket # No title change or error (log?)
      end

    {:noreply,
     socket
     |> stream_insert(:messages, ai_message, at: -1) # Add AI message to the stream
     |> assign(:sending_message, false) # Hide spinner
     |> scroll_chat_to_bottom() # Scroll down
    }
  end

  @impl true
  def handle_info({:ai_response, {:error, type, details}}, socket) do
    IO.inspect({type, details}, label: "AI Response Error")
    {:noreply,
      socket
      |> assign(:sending_message, false)
      |> put_flash(:error, "Error getting AI response: #{type}. Check logs.")}
  end

  defp page_title(nil), do: "Chat"
  defp page_title(""), do: "Chat"
  defp page_title(title), do: "Chat: #{title}"

  defp scroll_chat_to_bottom(socket) do
    push_event(socket, "js-scroll-bottom", %{to: "#chat-container"})
  end

  defp send_to_ai_and_reply(live_view_pid, session_id, user_message, history_for_ai) do
    try do
      case AiClient.get_ai_response(history_for_ai) do
        {:ok, ai_text} ->
          chat_session = Chat.get_chat_session!(session_id)

          case Chat.create_message(chat_session, "ai", ai_text) do
            {:ok, ai_message} ->
              title_update_result = maybe_generate_and_update_title(chat_session, user_message, ai_message)
              send(live_view_pid, {:ai_response, {:ok, ai_message, title_update_result}})
            {:error, changeset} ->
              send(live_view_pid, {:ai_response, {:error, :db_save_error, changeset}})
          end

        {:error, reason} ->
          send(live_view_pid, {:ai_response, {:error, :ai_api_error, reason}})
      end
    catch
      Ecto.NoResultsError ->
         send(live_view_pid, {:ai_response, {:error, :session_not_found_on_fetch, session_id}})
    end
  end

  defp maybe_generate_and_update_title(%ChatSession{} = session, user_message, ai_message) do
    if is_nil(session.title) || session.title == "" do
      case AiClient.generate_title(user_message, ai_message) do
        {:ok, generated_title} ->
           case Chat.update_chat_session(session, %{title: generated_title}) do
             {:ok, updated_session} -> {:ok, updated_session.title}
             {:error, _changeset} -> {:error, :title_db_update_failed}
           end
        {:error, _reason} -> {:error, :title_generation_failed}
      end
    else
      {:ok, nil}
    end
  end
end
