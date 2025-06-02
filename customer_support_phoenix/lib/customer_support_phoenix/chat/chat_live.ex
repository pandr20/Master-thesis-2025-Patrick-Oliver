defmodule CustomerSupportPhoenix.Chat.ChatLive do
  use Ecto.Schema
  import Ecto.Changeset

  schema "chat_sessions" do
    field :title, :string

    timestamps(type: :utc_datetime)
  end

  @doc false
  def changeset(chat_live, attrs) do
    chat_live
    |> cast(attrs, [:title])
    |> validate_required([:title])
  end
end
