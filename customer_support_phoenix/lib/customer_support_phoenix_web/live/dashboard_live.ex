defmodule CustomerSupportPhoenixWeb.DashboardLive do
  use CustomerSupportPhoenixWeb, :live_view

  alias CustomerSupportPhoenix.Chat

  @impl true
  def mount(_params, _session, socket) do
    stats = Chat.get_dashboard_stats()
    recent_feedback = Chat.list_recent_feedback() # Uses default limit of 5

    # Calculate positive rate, handling division by zero
    positive_rate =
      if stats.total_feedback > 0 do
        Float.round((stats.positive_ratings / stats.total_feedback) * 100)
      else
        0
      end

    {:ok,
      socket
      |> assign(:page_title, "Dashboard")
      |> assign(:stats, stats)
      |> assign(:recent_feedback, recent_feedback)
      |> assign(:positive_rate, positive_rate)
    }
  end

  @impl true
  def render(assigns) do
    ~H"""
    <%!-- Main container with dark background - NO <Layouts.app> wrapper needed anymore --%>
    <div class="p-4 sm:p-6 lg:p-8 bg-gray-900 min-h-screen text-gray-300">
      <h1 class="text-2xl font-semibold text-gray-100 mb-6">AI Chat Feedback</h1>

      <%!-- Stats Cards --%>
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-5 mb-8">
        <.stat_card title="Total Feedback" value={@stats.total_feedback} />
        <.stat_card title="Positive Ratings" value={@stats.positive_ratings} />
        <.stat_card title="Negative Ratings" value={@stats.negative_ratings} />
        <.stat_card title="Positive Rate" value={to_string(@positive_rate) <> "%"} />
        <.stat_card title="Total Chats" value={@stats.total_chats} />
      </div>

      <%!-- Recent Feedback Table --%>
      <h2 class="text-xl font-semibold text-gray-100 mb-4">Recent Feedback</h2>
      <%!-- Table container with dark background --%>
      <div class="overflow-x-auto bg-gray-800 shadow rounded-lg">
        <table class="min-w-full divide-y divide-gray-700">
          <%!-- Darker table header --%>
          <thead class="bg-gray-900">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Rating</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">AI Message</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Comment</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Date</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Action</th>
            </tr>
          </thead>
          <%!-- Table body with dark background and light text --%>
          <tbody class="bg-gray-800 divide-y divide-gray-700">
            <tr :for={feedback <- @recent_feedback}>
              <td class="px-6 py-4 whitespace-nowrap">
                <%!-- Rating badges - Adjusted for contrast --%>
                <span class={[
                  "px-2 inline-flex text-xs leading-5 font-semibold rounded-full",
                  feedback.rating == "positive" && "bg-green-200 text-green-900",
                  feedback.rating == "negative" && "bg-red-200 text-red-900"
                  ]}>
                  {feedback.rating |> String.capitalize()}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-300 truncate max-w-xs">{feedback.chat_message.message}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{feedback.comment || "-"}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                <%!-- Placeholder - Need User context --%>
                Patrick Andreassen
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-400">
                 {DateTime.shift_zone!(feedback.inserted_at, "Etc/UTC") |> Calendar.strftime("%d/%m/%Y, %H:%M:%S")}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <.link navigate={~p"/chat/#{feedback.chat_message.chat_session_id}"} class="text-indigo-400 hover:text-indigo-300">
                  <CustomerSupportPhoenixWeb.CoreComponents.icon name="hero-arrow-top-right-on-square" class="h-5 w-5" />
                </.link>
              </td>
            </tr>
            <tr :if={@recent_feedback == []}>
              <td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500">No feedback submitted yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    """
  end

  # Simple Stat Card Component (needs dark mode adjustments)
  defp stat_card(assigns) do
    ~H"""
    <%!-- Stat card with dark background and light text --%>
    <div class="bg-gray-800 overflow-hidden shadow rounded-lg">
      <div class="p-5">
        <dt class="text-sm font-medium text-gray-400 truncate">{@title}</dt>
        <dd class="mt-1 text-3xl font-semibold text-gray-100">{@value}</dd>
      </div>
    </div>
    """
  end
end
