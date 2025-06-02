defmodule CustomerSupportPhoenix.ChatFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `CustomerSupportPhoenix.Chat` context.
  """

  @doc """
  Generate a chat_session.
  """
  def chat_session_fixture(attrs \\ %{}) do
    {:ok, chat_session} =
      attrs
      |> Enum.into(%{
        title: "some title"
      })
      |> CustomerSupportPhoenix.Chat.create_chat_session()

    chat_session
  end

  @doc """
  Generate a chat_message.
  """
  def chat_message_fixture(attrs \\ %{}) do
    {:ok, chat_message} =
      attrs
      |> Enum.into(%{
        message: "some message",
        sender: "some sender"
      })
      |> CustomerSupportPhoenix.Chat.create_chat_message()

    chat_message
  end

  @doc """
  Generate a chat_message_feedback.
  """
  def chat_message_feedback_fixture(attrs \\ %{}) do
    {:ok, chat_message_feedback} =
      attrs
      |> Enum.into(%{
        comment: "some comment",
        rating: "some rating"
      })
      |> CustomerSupportPhoenix.Chat.create_chat_message_feedback()

    chat_message_feedback
  end

  @doc """
  Generate a chat_live.
  """
  def chat_live_fixture(attrs \\ %{}) do
    {:ok, chat_live} =
      attrs
      |> Enum.into(%{
        title: "some title"
      })
      |> CustomerSupportPhoenix.Chat.create_chat_live()

    chat_live
  end
end
