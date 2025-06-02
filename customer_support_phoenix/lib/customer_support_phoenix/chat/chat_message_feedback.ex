defmodule CustomerSupportPhoenix.Chat.ChatMessageFeedback do
  use Ecto.Schema
  import Ecto.Changeset

  alias CustomerSupportPhoenix.Chat.ChatMessage

  schema "chat_message_feedbacks" do
    field :rating, :string
    field :comment, :string
    belongs_to :chat_message, ChatMessage

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(chat_message_feedback, attrs) do
    chat_message_feedback
    |> cast(attrs, [:rating, :comment, :chat_message_id])
    |> validate_required([:rating, :comment, :chat_message_id])
  end
end
