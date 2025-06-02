defmodule CustomerSupportPhoenix.ChatTest do
  use CustomerSupportPhoenix.DataCase

  alias CustomerSupportPhoenix.Chat

  describe "chat_sessions" do
    alias CustomerSupportPhoenix.Chat.ChatSession

    import CustomerSupportPhoenix.ChatFixtures

    @invalid_attrs %{title: nil}

    test "list_chat_sessions/0 returns all chat_sessions" do
      chat_session = chat_session_fixture()
      assert Chat.list_chat_sessions() == [chat_session]
    end

    test "get_chat_session!/1 returns the chat_session with given id" do
      chat_session = chat_session_fixture()
      assert Chat.get_chat_session!(chat_session.id) == chat_session
    end

    test "create_chat_session/1 with valid data creates a chat_session" do
      valid_attrs = %{title: "some title"}

      assert {:ok, %ChatSession{} = chat_session} = Chat.create_chat_session(valid_attrs)
      assert chat_session.title == "some title"
    end

    test "create_chat_session/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Chat.create_chat_session(@invalid_attrs)
    end

    test "update_chat_session/2 with valid data updates the chat_session" do
      chat_session = chat_session_fixture()
      update_attrs = %{title: "some updated title"}

      assert {:ok, %ChatSession{} = chat_session} = Chat.update_chat_session(chat_session, update_attrs)
      assert chat_session.title == "some updated title"
    end

    test "update_chat_session/2 with invalid data returns error changeset" do
      chat_session = chat_session_fixture()
      assert {:error, %Ecto.Changeset{}} = Chat.update_chat_session(chat_session, @invalid_attrs)
      assert chat_session == Chat.get_chat_session!(chat_session.id)
    end

    test "delete_chat_session/1 deletes the chat_session" do
      chat_session = chat_session_fixture()
      assert {:ok, %ChatSession{}} = Chat.delete_chat_session(chat_session)
      assert_raise Ecto.NoResultsError, fn -> Chat.get_chat_session!(chat_session.id) end
    end

    test "change_chat_session/1 returns a chat_session changeset" do
      chat_session = chat_session_fixture()
      assert %Ecto.Changeset{} = Chat.change_chat_session(chat_session)
    end
  end

  describe "chat_messages" do
    alias CustomerSupportPhoenix.Chat.ChatMessage

    import CustomerSupportPhoenix.ChatFixtures

    @invalid_attrs %{message: nil, sender: nil}

    test "list_chat_messages/0 returns all chat_messages" do
      chat_message = chat_message_fixture()
      assert Chat.list_chat_messages() == [chat_message]
    end

    test "get_chat_message!/1 returns the chat_message with given id" do
      chat_message = chat_message_fixture()
      assert Chat.get_chat_message!(chat_message.id) == chat_message
    end

    test "create_chat_message/1 with valid data creates a chat_message" do
      valid_attrs = %{message: "some message", sender: "some sender"}

      assert {:ok, %ChatMessage{} = chat_message} = Chat.create_chat_message(valid_attrs)
      assert chat_message.message == "some message"
      assert chat_message.sender == "some sender"
    end

    test "create_chat_message/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Chat.create_chat_message(@invalid_attrs)
    end

    test "update_chat_message/2 with valid data updates the chat_message" do
      chat_message = chat_message_fixture()
      update_attrs = %{message: "some updated message", sender: "some updated sender"}

      assert {:ok, %ChatMessage{} = chat_message} = Chat.update_chat_message(chat_message, update_attrs)
      assert chat_message.message == "some updated message"
      assert chat_message.sender == "some updated sender"
    end

    test "update_chat_message/2 with invalid data returns error changeset" do
      chat_message = chat_message_fixture()
      assert {:error, %Ecto.Changeset{}} = Chat.update_chat_message(chat_message, @invalid_attrs)
      assert chat_message == Chat.get_chat_message!(chat_message.id)
    end

    test "delete_chat_message/1 deletes the chat_message" do
      chat_message = chat_message_fixture()
      assert {:ok, %ChatMessage{}} = Chat.delete_chat_message(chat_message)
      assert_raise Ecto.NoResultsError, fn -> Chat.get_chat_message!(chat_message.id) end
    end

    test "change_chat_message/1 returns a chat_message changeset" do
      chat_message = chat_message_fixture()
      assert %Ecto.Changeset{} = Chat.change_chat_message(chat_message)
    end
  end

  describe "chat_message_feedbacks" do
    alias CustomerSupportPhoenix.Chat.ChatMessageFeedback

    import CustomerSupportPhoenix.ChatFixtures

    @invalid_attrs %{comment: nil, rating: nil}

    test "list_chat_message_feedbacks/0 returns all chat_message_feedbacks" do
      chat_message_feedback = chat_message_feedback_fixture()
      assert Chat.list_chat_message_feedbacks() == [chat_message_feedback]
    end

    test "get_chat_message_feedback!/1 returns the chat_message_feedback with given id" do
      chat_message_feedback = chat_message_feedback_fixture()
      assert Chat.get_chat_message_feedback!(chat_message_feedback.id) == chat_message_feedback
    end

    test "create_chat_message_feedback/1 with valid data creates a chat_message_feedback" do
      valid_attrs = %{comment: "some comment", rating: "some rating"}

      assert {:ok, %ChatMessageFeedback{} = chat_message_feedback} = Chat.create_chat_message_feedback(valid_attrs)
      assert chat_message_feedback.comment == "some comment"
      assert chat_message_feedback.rating == "some rating"
    end

    test "create_chat_message_feedback/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Chat.create_chat_message_feedback(@invalid_attrs)
    end

    test "update_chat_message_feedback/2 with valid data updates the chat_message_feedback" do
      chat_message_feedback = chat_message_feedback_fixture()
      update_attrs = %{comment: "some updated comment", rating: "some updated rating"}

      assert {:ok, %ChatMessageFeedback{} = chat_message_feedback} = Chat.update_chat_message_feedback(chat_message_feedback, update_attrs)
      assert chat_message_feedback.comment == "some updated comment"
      assert chat_message_feedback.rating == "some updated rating"
    end

    test "update_chat_message_feedback/2 with invalid data returns error changeset" do
      chat_message_feedback = chat_message_feedback_fixture()
      assert {:error, %Ecto.Changeset{}} = Chat.update_chat_message_feedback(chat_message_feedback, @invalid_attrs)
      assert chat_message_feedback == Chat.get_chat_message_feedback!(chat_message_feedback.id)
    end

    test "delete_chat_message_feedback/1 deletes the chat_message_feedback" do
      chat_message_feedback = chat_message_feedback_fixture()
      assert {:ok, %ChatMessageFeedback{}} = Chat.delete_chat_message_feedback(chat_message_feedback)
      assert_raise Ecto.NoResultsError, fn -> Chat.get_chat_message_feedback!(chat_message_feedback.id) end
    end

    test "change_chat_message_feedback/1 returns a chat_message_feedback changeset" do
      chat_message_feedback = chat_message_feedback_fixture()
      assert %Ecto.Changeset{} = Chat.change_chat_message_feedback(chat_message_feedback)
    end
  end

  describe "chat_sessions" do
    alias CustomerSupportPhoenix.Chat.ChatLive

    import CustomerSupportPhoenix.ChatFixtures

    @invalid_attrs %{title: nil}

    test "list_chat_sessions/0 returns all chat_sessions" do
      chat_live = chat_live_fixture()
      assert Chat.list_chat_sessions() == [chat_live]
    end

    test "get_chat_live!/1 returns the chat_live with given id" do
      chat_live = chat_live_fixture()
      assert Chat.get_chat_live!(chat_live.id) == chat_live
    end

    test "create_chat_live/1 with valid data creates a chat_live" do
      valid_attrs = %{title: "some title"}

      assert {:ok, %ChatLive{} = chat_live} = Chat.create_chat_live(valid_attrs)
      assert chat_live.title == "some title"
    end

    test "create_chat_live/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Chat.create_chat_live(@invalid_attrs)
    end

    test "update_chat_live/2 with valid data updates the chat_live" do
      chat_live = chat_live_fixture()
      update_attrs = %{title: "some updated title"}

      assert {:ok, %ChatLive{} = chat_live} = Chat.update_chat_live(chat_live, update_attrs)
      assert chat_live.title == "some updated title"
    end

    test "update_chat_live/2 with invalid data returns error changeset" do
      chat_live = chat_live_fixture()
      assert {:error, %Ecto.Changeset{}} = Chat.update_chat_live(chat_live, @invalid_attrs)
      assert chat_live == Chat.get_chat_live!(chat_live.id)
    end

    test "delete_chat_live/1 deletes the chat_live" do
      chat_live = chat_live_fixture()
      assert {:ok, %ChatLive{}} = Chat.delete_chat_live(chat_live)
      assert_raise Ecto.NoResultsError, fn -> Chat.get_chat_live!(chat_live.id) end
    end

    test "change_chat_live/1 returns a chat_live changeset" do
      chat_live = chat_live_fixture()
      assert %Ecto.Changeset{} = Chat.change_chat_live(chat_live)
    end
  end
end
