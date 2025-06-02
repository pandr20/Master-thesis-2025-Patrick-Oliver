defmodule CustomerSupportPhoenixWeb.ChatLiveLive.Index do
  use CustomerSupportPhoenixWeb, :live_view

  alias CustomerSupportPhoenix.Chat
  alias CustomerSupportPhoenix.Chat.ChatSession

  @impl true
  def mount(_params, _session, socket) do
    {:ok,
     socket
     |> assign(:page_title, "Chat Sessions")
     |> stream(:chat_sessions, Chat.list_chat_sessions(), dom_id: fn session -> "chat-session-#{session.id}" end)
    }
  end

  @impl true
  def handle_event("new_chat_session", _, socket) do
    case Chat.create_chat_session(%{title: "New Chat Session"}) do
      {:ok, chat_session} ->
        {:noreply,
         socket
         |> put_flash(:info, "New chat created.")
         |> push_navigate(to: ~p"/chat/#{chat_session.id}")
        }
      {:error, _changeset} ->
        {:noreply, put_flash(socket, :error, "Failed to create chat session.")}
    end
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    try do
      chat_session = Chat.get_chat_session!(id)
      case Chat.delete_chat_session(chat_session) do
        {:ok, _deleted_session} ->
          {:noreply, stream_delete(socket, :chat_sessions, chat_session)}
        {:error, _changeset} ->
          {:noreply, put_flash(socket, :error, "Failed to delete chat session.")}
      end
    catch
      Ecto.NoResultsError ->
        # Session was not found (already deleted or invalid ID)
        {:noreply, socket}
    end
  end

  defp js_delete_session(dom_id, chat_session) do
    JS.push("delete", value: %{id: chat_session.id})
    |> JS.hide(to: "#" <> dom_id)
  end

  defp js_navigate_to_session({_id, chat_session}) do
    JS.navigate(~p"/chat/#{chat_session.id}")
  end
end
