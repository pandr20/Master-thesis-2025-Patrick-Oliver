defmodule CustomerSupportPhoenix.AiClient do
  @moduledoc """
  Handles communication with the external AI service.
  """

  alias Req

  # Helper function to get the configured API key
  defp get_api_key do
    Application.fetch_env!(:customer_support_phoenix, :gemini_api_key)
    # Or use fetch_env if you want to handle the :error case explicitly
    # Application.fetch_env(:customer_support_phoenix, :gemini_api_key)
  end

  # Define the API endpoint - could also be moved to config
  @api_url "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"

  @doc """
  Gets a chat completion response from the AI.

  Takes a list of message maps (e.g., `[%{sender: "user", message: "Hello"}, %{sender: "ai", message: "Hi there!"}]`)
  Returns `{:ok, ai_response_text}` or `{:error, reason}`.
  """
  def get_ai_response(messages_history) do
    # Fetch the API key from config
    api_key = get_api_key()

    # Ensure API key is present
    if is_nil(api_key) or api_key == "" do
      # Return an error or use placeholder if running without a key
      IO.puts(:stderr, "GEMINI_API_KEY not configured. Using placeholder response.")
      Process.sleep(500)
      {:ok, "Placeholder AI response (API key missing)."}
    else
      # Prepare the request body according to Gemini API spec
      body = %{
        contents: format_messages_for_gemini(messages_history)
        # Add generationConfig if needed, e.g.:
        # generationConfig: %{
        #   temperature: 0.7,
        #   topP: 1,
        #   topK: 1,
        #   maxOutputTokens: 2048
        # }
      }

      full_api_url = @api_url <> "?key=" <> api_key
      IO.inspect(body, label: "Sending to AI (#{@api_url})")

      case Req.post(full_api_url, json: body) do
        {:ok, %Req.Response{status: 200, body: response_body}} ->
           # Use List.first/hd for safe access instead of index [0]
           # Add checks for nil if the structure might be missing
           candidate = List.first(response_body["candidates"])
           part = candidate && List.first(candidate["content"]["parts"])
           ai_text = part && part["text"]

           # TODO: Add more robust error handling if candidate, part, or text is nil
           if ai_text do
            {:ok, ai_text}
           else
             IO.inspect(response_body, label: "AI API Response Missing Expected Structure")
             {:error, :response_format_error}
           end
        {:ok, resp} ->
          IO.inspect(resp, label: "AI API Error Response")
          {:error, {:api_error, resp.status, resp.body}}
        {:error, reason} ->
          IO.inspect(reason, label: "AI HTTP Error")
          {:error, {:http_error, reason}}
      end
    end
  end

  @doc """
  Generates a short, descriptive title for a chat session based on the initial messages.

  Takes the first user message and potentially the first AI response.
  Returns `{:ok, title}` or `{:error, reason}`.
  """
  def generate_title(first_user_message, _first_ai_message \\ nil) do
    # Fetch the API key from config
    api_key = get_api_key()

    if is_nil(api_key) or api_key == "" do
      IO.puts(:stderr, "GEMINI_API_KEY not configured. Using placeholder title.")
      Process.sleep(100)
      {:ok, "Placeholder Title (No API Key)"}
    else
      # Construct a simple prompt for title generation
      prompt = "Generate a very short, concise title (max 5 words) for a chat session starting with this user message: '#{first_user_message.message}'"

      # Use the same endpoint, just with a different payload structure
      body = %{
        contents: [%{role: "user", parts: [%{text: prompt}]}]
      }

      full_api_url = @api_url <> "?key=" <> api_key
      IO.inspect(body, label: "Sending Title Gen to AI (#{@api_url})")

      case Req.post(full_api_url, json: body) do
        {:ok, %Req.Response{status: 200, body: response_body}} ->
          # TODO: Robust error handling
          title = response_body["candidates"][0]["content"]["parts"][0]["text"]
          {:ok, String.trim(title)}
        {:ok, resp} ->
          IO.inspect(resp, label: "AI Title Gen Error Response")
          {:error, {:api_error, resp.status, resp.body}}
        {:error, reason} ->
          IO.inspect(reason, label: "AI Title Gen HTTP Error")
          {:error, {:http_error, reason}}
      end
    end
  end

  # Helper function to convert our message format to Gemini API format
  defp format_messages_for_gemini(messages) do
    Enum.map(messages, fn msg ->
      role = if msg.sender == "user", do: "user", else: "model"
      %{role: role, parts: [%{text: msg.message}]}
    end)
  end
end
