# frozen_string_literal: true
require 'net/http'
class ChatboxController < ApplicationController

  def index
    @conversation = Conversation.last
    @messages = @conversation&.messages
  end





end
