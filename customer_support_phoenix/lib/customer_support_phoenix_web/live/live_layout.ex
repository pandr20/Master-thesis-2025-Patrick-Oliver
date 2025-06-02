defmodule CustomerSupportPhoenixWeb.LiveLayout do
  use CustomerSupportPhoenixWeb, :live_view

  alias CustomerSupportPhoenixWeb.Layouts # Keep access to flash_group, theme_toggle if needed
  alias CustomerSupportPhoenixWeb.CoreComponents

  # This layout is simple and doesn't need mount/handle_params for now.
  # It just renders the persistent structure.

  def render(assigns) do
    # Temporarily inspect the socket to find the URI/path
    # IO.inspect(@socket, label: "Socket in LiveLayout render") # Can remove this debug line now

    ~H"""
    <%!-- Persistent Header/Navbar --%>
    <header class="navbar px-4 sm:px-6 lg:px-8 bg-base-200 text-base-content sticky top-0 z-40 border-b border-base-300">
      <div class="flex-1">
        <a href={~p"/"} class="flex-1 flex items-center gap-2">
          <%!-- Assuming logo.svg exists --%>
          <img src={~p"/images/logo.svg"} width="36" alt="App Logo"/>
          <span class="text-sm font-semibold">v{Application.spec(:phoenix, :vsn)}</span>
        </a>
      </div>
      <div class="flex-none">
        <ul class="flex flex-row px-1 space-x-4 items-center">
          <li>
            <.link href={~p"/dashboard"} class="btn btn-ghost">
              Dashboard
            </.link>
          </li>
          <li>
            <.link href={~p"/chat"} class="btn btn-ghost">
              Chats
            </.link>
          </li>
          <li>
            <a href="https://phoenixframework.org/" class="btn btn-ghost" target="_blank" rel="noopener noreferrer">Website</a>
          </li>
          <li>
            <a href="https://github.com/phoenixframework/phoenix" class="btn btn-ghost" target="_blank" rel="noopener noreferrer">GitHub</a>
          </li>
          <li>
            <Layouts.theme_toggle />
          </li>
          <li>
            <a href="https://hexdocs.pm/phoenix/overview.html" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
              Get Started <span aria-hidden="true">&rarr;</span>
            </a>
          </li>
        </ul>
      </div>
    </header>

    <%!-- Main content area where the actual LiveView content will be injected --%>
    <main class="px-4 py-10 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl"> <%!-- Adjusted max-width for potentially wider content --%>
         <%= @inner_content %>
      </div>
    </main>

    <%!-- Flash messages can stay here or move to root layout if preferred --%>
    <Layouts.flash_group flash={@flash} />
    """
  end

  # Helper to check the current path for active link styling - REMOVED
  # defp current_path?(socket, path) do
  #   current_path = URI.parse(socket.uri).path
  #   current_path == path
  # end
end
