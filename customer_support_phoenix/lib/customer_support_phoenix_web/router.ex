defmodule CustomerSupportPhoenixWeb.Router do
  use CustomerSupportPhoenixWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, html: {CustomerSupportPhoenixWeb.Layouts, :root}
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CustomerSupportPhoenixWeb do
    pipe_through :browser

    # Use the LiveLayout for these routes
    live_session :default,
                  layout: {CustomerSupportPhoenixWeb.LiveLayout, :render} do

      live "/dashboard", DashboardLive
      live "/chat", ChatLiveLive.Index, :index
      live "/chat/:id", ChatLiveLive.Show, :show
    end

    # Routes that should NOT use the LiveLayout (if any)
    get "/", PageController, :home # Example: Home page might use a different layout or none

  end

  # Other scopes may use custom stacks.
  # scope "/api", CustomerSupportPhoenixWeb do
  #   pipe_through :api
  # end

  # Enable LiveDashboard and Swoosh mailbox preview in development
  if Application.compile_env(:customer_support_phoenix, :dev_routes) do
    # If you want to use the LiveDashboard in production, you should put
    # it behind authentication and allow only admins to access it.
    # If your application does not have an admins-only section yet,
    # you can use Plug.BasicAuth to set up some basic authentication
    # as long as you are also using SSL (which you should anyway).
    import Phoenix.LiveDashboard.Router

    scope "/dev" do
      pipe_through :browser

      live_dashboard "/dashboard", metrics: CustomerSupportPhoenixWeb.Telemetry
      forward "/mailbox", Plug.Swoosh.MailboxPreview
    end
  end
end
