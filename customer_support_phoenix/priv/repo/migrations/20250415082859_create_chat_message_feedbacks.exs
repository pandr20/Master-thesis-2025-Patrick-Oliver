defmodule CustomerSupportPhoenix.Repo.Migrations.CreateChatMessageFeedbacks do
  use Ecto.Migration

  def change do
    create table(:chat_message_feedbacks) do
      add :rating, :string
      add :comment, :text
      add :chat_message_id, references(:chat_messages, on_delete: :nothing)

      timestamps(type: :utc_datetime)
    end

    create index(:chat_message_feedbacks, [:chat_message_id])
  end
end
