defmodule CustomerSupportPhoenix.Chat.ChatSession do
  use Ecto.Schema
  import Ecto.Changeset

  alias CustomerSupportPhoenix.Chat.ChatMessage

  schema "chat_sessions" do
    field :title, :string
    has_many :messages, ChatMessage

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(chat_session, attrs) do
    chat_session
    |> cast(attrs, [:title])
    |> validate_required([:title])
  end
end
