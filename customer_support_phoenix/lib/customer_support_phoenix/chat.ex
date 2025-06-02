defmodule CustomerSupportPhoenix.Chat do
  @moduledoc """
  The Chat context.
  """

  import Ecto.Query, warn: false
  alias CustomerSupportPhoenix.Repo

  alias CustomerSupportPhoenix.Chat.ChatSession
  alias CustomerSupportPhoenix.Chat.ChatMessage
  alias CustomerSupportPhoenix.Chat.ChatMessageFeedback

  @doc """
  Returns the list of chat_sessions.

  ## Examples

      iex> list_chat_sessions()
      [%ChatSession{}, ...]

  """
  def list_chat_sessions do
    Repo.all(ChatSession)
  end

  @doc """
  Gets a single chat_session.

  Raises `Ecto.NoResultsError` if the Chat session does not exist.

  ## Examples

      iex> get_chat_session!(123)
      %ChatSession{}

      iex> get_chat_session!(456)
      ** (Ecto.NoResultsError)

  """
  def get_chat_session!(id), do: Repo.get!(ChatSession, id)

  @doc """
  Gets a single chat_session and preloads its messages and their feedback.

  Raises `Ecto.NoResultsError` if the Chat session does not exist.

  ## Examples

      iex> get_chat_session_with_messages!(123)
      %ChatSession{messages: [%ChatMessage{feedback: %ChatMessageFeedback{}}, ...]}

      iex> get_chat_session_with_messages!(456)
      ** (Ecto.NoResultsError)

  """
  def get_chat_session_with_messages!(id) do
    ChatSession
    |> Repo.get!(id)
    |> Repo.preload(messages: [feedback: :chat_message])
    |> case do
      %{messages: messages} = session ->
        # Sort messages by insertion time
        messages_sorted = Enum.sort_by(messages, &(&1.inserted_at))
        %{session | messages: messages_sorted}
      nil ->
        # Should not happen due to get! above, but handles the structure
        nil
    end
  end

  @doc """
  Creates a chat_session.

  ## Examples

      iex> create_chat_session(%{field: value})
      {:ok, %ChatSession{}}

      iex> create_chat_session(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_chat_session(attrs \\ %{}) do
    %ChatSession{}
    |> ChatSession.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a chat_session.

  ## Examples

      iex> update_chat_session(chat_session, %{field: new_value})
      {:ok, %ChatSession{}}

      iex> update_chat_session(chat_session, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_chat_session(%ChatSession{} = chat_session, attrs) do
    chat_session
    |> ChatSession.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a chat_session and associated messages/feedback.

  ## Examples

      iex> delete_chat_session(chat_session)
      {:ok, %ChatSession{}}

      iex> delete_chat_session(chat_session)
      {:error, %Ecto.Changeset{}}

  """
  def delete_chat_session(%ChatSession{} = chat_session) do
    # Consider adding transaction for safety
    Repo.delete(chat_session)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking chat_session changes.

  ## Examples

      iex> change_chat_session(chat_session)
      %Ecto.Changeset{data: %ChatSession{}}

  """
  def change_chat_session(%ChatSession{} = chat_session, attrs \\ %{}) do
    ChatSession.changeset(chat_session, attrs)
  end

  @doc """
  Gets a single chat_message.

  Raises `Ecto.NoResultsError` if the Chat message does not exist.

  ## Examples

      iex> get_chat_message!(123)
      %ChatMessage{}

      iex> get_chat_message!(456)
      ** (Ecto.NoResultsError)

  """
  def get_chat_message!(id), do: Repo.get!(ChatMessage, id) |> Repo.preload([:feedback])

  @doc """
  Creates a chat message associated with a chat session.

  ## Examples

      iex> create_message(chat_session, "user", "Hello there")
      {:ok, %ChatMessage{}}

      iex> create_message(chat_session, "invalid_sender", "")
      {:error, %Ecto.Changeset{}}

  """
  def create_message(%ChatSession{} = chat_session, sender, message_text) do
    %ChatMessage{}
    |> ChatMessage.changeset(%{sender: sender, message: message_text, chat_session_id: chat_session.id})
    |> Repo.insert()
  end

  @doc """
  Retrieves statistics for the dashboard.

  Returns a map containing:
  - :total_feedback
  - :positive_ratings
  - :negative_ratings
  - :total_chats
  """
  def get_dashboard_stats do
    # Aliases are convenient but Repo functions often need the full module name
    # alias CustomerSupportPhoenix.Chat.{ChatMessage, ChatMessageFeedback}

    # Ensure all aggregate calls use an Ecto.Query struct from `from`
    total_feedback = Repo.aggregate(from(f in CustomerSupportPhoenix.Chat.ChatMessageFeedback), :count, :id)
    positive_ratings = Repo.aggregate(from(f in CustomerSupportPhoenix.Chat.ChatMessageFeedback, where: f.rating == "positive"), :count, :id)
    negative_ratings = Repo.aggregate(from(f in CustomerSupportPhoenix.Chat.ChatMessageFeedback, where: f.rating == "negative"), :count, :id)
    total_chats = Repo.aggregate(from(s in CustomerSupportPhoenix.Chat.ChatSession), :count, :id)

    %{
      total_feedback: total_feedback,
      positive_ratings: positive_ratings,
      negative_ratings: negative_ratings,
      total_chats: total_chats
    }
  end

  @doc """
  Lists recent feedback entries with associated message and user info.
  """
  def list_recent_feedback(limit \\ 5) do
    # Use the correct module name: ChatMessageFeedback
    alias CustomerSupportPhoenix.Chat.ChatMessageFeedback

    # Assuming User schema exists and is linked implicitly or explicitly elsewhere
    # If User association is explicitly defined on Feedback, preload it.
    # Adjust preload path if needed (e.g., [:chat_message, :user] if user is on message)
    query =
      from f in ChatMessageFeedback,
      order_by: [desc: f.inserted_at],
      limit: ^limit,
      preload: [:chat_message] # Preload message, assuming user info is not directly linked here
      # If User is linked to Feedback: preload: [:chat_message, :user]

    Repo.all(query)
    # You might need to fetch User info separately if not directly linked/preloaded,
    # or adjust the query/preloading based on your exact schema relationships.
  end

  @doc """
  Creates or updates feedback for a given AI message.

  ## Examples
      iex> create_or_update_feedback(ai_message, %{rating: "positive", comment: "Helpful!"})
      {:ok, %ChatMessageFeedback{}}

      iex> create_or_update_feedback(ai_message, %{rating: "invalid"})
      {:error, %Ecto.Changeset{}}

  """
  def create_or_update_feedback(%ChatMessage{id: message_id, sender: "ai"} = _ai_message, attrs) do
     feedback_attrs = Map.put(attrs, :chat_message_id, message_id)

     case Repo.get_by(ChatMessageFeedback, chat_message_id: message_id) do
      nil ->
        # Create new feedback
        %ChatMessageFeedback{}
        |> ChatMessageFeedback.changeset(feedback_attrs)
        |> Repo.insert()
      existing_feedback ->
        # Update existing feedback
        existing_feedback
        |> ChatMessageFeedback.changeset(feedback_attrs)
        |> Repo.update()
      end
  end

  def create_or_update_feedback(%ChatMessage{sender: "user"}, _attrs) do
     # Cannot add feedback to user messages
     {:error, :cannot_add_feedback_to_user_message}
  end
end
