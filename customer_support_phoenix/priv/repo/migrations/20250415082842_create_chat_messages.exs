defmodule CustomerSupportPhoenix.Repo.Migrations.CreateChatMessages do
  use Ecto.Migration

  def change do
    create table(:chat_messages) do
      add :sender, :string
      add :message, :text
      add :chat_session_id, references(:chat_sessions, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:chat_messages, [:chat_session_id])
  end
end
