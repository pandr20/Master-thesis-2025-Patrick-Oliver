defmodule CustomerSupportPhoenixWeb.ChatLiveLiveTest do
  use CustomerSupportPhoenixWeb.ConnCase

  import Phoenix.LiveViewTest
  import CustomerSupportPhoenix.ChatFixtures

  @create_attrs %{title: "some title"}
  @update_attrs %{title: "some updated title"}
  @invalid_attrs %{title: nil}
  defp create_chat_live(_) do
    chat_live = chat_live_fixture()

    %{chat_live: chat_live}
  end

  describe "Index" do
    setup [:create_chat_live]

    test "lists all chat_sessions", %{conn: conn, chat_live: chat_live} do
      {:ok, _index_live, html} = live(conn, ~p"/chat_sessions")

      assert html =~ "Listing Chat sessions"
      assert html =~ chat_live.title
    end

    test "saves new chat_live", %{conn: conn} do
      {:ok, index_live, _html} = live(conn, ~p"/chat_sessions")

      assert {:ok, form_live, _} =
               index_live
               |> element("a", "New Chat live")
               |> render_click()
               |> follow_redirect(conn, ~p"/chat_sessions/new")

      assert render(form_live) =~ "New Chat live"

      assert form_live
             |> form("#chat_live-form", chat_live: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      assert {:ok, index_live, _html} =
               form_live
               |> form("#chat_live-form", chat_live: @create_attrs)
               |> render_submit()
               |> follow_redirect(conn, ~p"/chat_sessions")

      html = render(index_live)
      assert html =~ "Chat live created successfully"
      assert html =~ "some title"
    end

    test "updates chat_live in listing", %{conn: conn, chat_live: chat_live} do
      {:ok, index_live, _html} = live(conn, ~p"/chat_sessions")

      assert {:ok, form_live, _html} =
               index_live
               |> element("#chat_sessions-#{chat_live.id} a", "Edit")
               |> render_click()
               |> follow_redirect(conn, ~p"/chat_sessions/#{chat_live}/edit")

      assert render(form_live) =~ "Edit Chat live"

      assert form_live
             |> form("#chat_live-form", chat_live: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      assert {:ok, index_live, _html} =
               form_live
               |> form("#chat_live-form", chat_live: @update_attrs)
               |> render_submit()
               |> follow_redirect(conn, ~p"/chat_sessions")

      html = render(index_live)
      assert html =~ "Chat live updated successfully"
      assert html =~ "some updated title"
    end

    test "deletes chat_live in listing", %{conn: conn, chat_live: chat_live} do
      {:ok, index_live, _html} = live(conn, ~p"/chat_sessions")

      assert index_live |> element("#chat_sessions-#{chat_live.id} a", "Delete") |> render_click()
      refute has_element?(index_live, "#chat_sessions-#{chat_live.id}")
    end
  end

  describe "Show" do
    setup [:create_chat_live]

    test "displays chat_live", %{conn: conn, chat_live: chat_live} do
      {:ok, _show_live, html} = live(conn, ~p"/chat_sessions/#{chat_live}")

      assert html =~ "Show Chat live"
      assert html =~ chat_live.title
    end

    test "updates chat_live and returns to show", %{conn: conn, chat_live: chat_live} do
      {:ok, show_live, _html} = live(conn, ~p"/chat_sessions/#{chat_live}")

      assert {:ok, form_live, _} =
               show_live
               |> element("a", "Edit")
               |> render_click()
               |> follow_redirect(conn, ~p"/chat_sessions/#{chat_live}/edit?return_to=show")

      assert render(form_live) =~ "Edit Chat live"

      assert form_live
             |> form("#chat_live-form", chat_live: @invalid_attrs)
             |> render_change() =~ "can&#39;t be blank"

      assert {:ok, show_live, _html} =
               form_live
               |> form("#chat_live-form", chat_live: @update_attrs)
               |> render_submit()
               |> follow_redirect(conn, ~p"/chat_sessions/#{chat_live}")

      html = render(show_live)
      assert html =~ "Chat live updated successfully"
      assert html =~ "some updated title"
    end
  end
end
