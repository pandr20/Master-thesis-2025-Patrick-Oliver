defmodule CustomerSupportPhoenix.Chat.ChatMessage do
  use Ecto.Schema
  import Ecto.Changeset

  alias CustomerSupportPhoenix.Chat.{ChatSession, ChatMessageFeedback}

  schema "chat_messages" do
    field :sender, :string
    field :message, :string
    belongs_to :chat_session, ChatSession
    has_one :feedback, ChatMessageFeedback

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(chat_message, attrs) do
    chat_message
    |> cast(attrs, [:sender, :message, :chat_session_id])
    |> validate_required([:sender, :message, :chat_session_id])
  end
end
