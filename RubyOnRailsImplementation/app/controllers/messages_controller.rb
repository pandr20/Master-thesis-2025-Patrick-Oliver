class MessagesController < ApplicationController
  def create
    puts "message_params: #{message_params}"

    @message = Message.new(message_params)
    @message.save

    response = make_request_to_chatbot
    @message = Message.new(content: response, conversation_id: @message.conversation_id, response: true)
    @message.save

    redirect_to conversation_path(@message.conversation)
  end

  def make_request_to_chatbot
    uri = URI('http://localhost:8000/chatbot')
    req = Net::HTTP::Post.new(uri, 'Content-Type' => 'application/json')
    req.body = { message: params[:message] }.to_json
    res = Net::HTTP.start(uri.hostname, uri.port) do |http|
      http.request(req)
    end
    JSON.parse(res.body)['message']
  end

  private

  def message_params
    params.require(:message).permit(:content, :conversation_id)
  end
end
