defmodule CustomerSupportPhoenix.Repo.Migrations.CreateChatSessions do
  use Ecto.Migration

  def change do
    create table(:chat_sessions) do
      add :title, :string

      timestamps(type: :utc_datetime)
    end
  end
end
