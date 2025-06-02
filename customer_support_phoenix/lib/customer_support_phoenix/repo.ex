defmodule CustomerSupportPhoenix.Repo do
  use Ecto.Repo,
    otp_app: :customer_support_phoenix,
    adapter: Ecto.Adapters.MyXQL
end
