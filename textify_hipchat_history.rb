#!/usr/bin/env ruby
# encoding: UTF-8
require 'nokogiri'

# Using HipChat's web interface, save the chat history as a web page (not
# an all-in-one file, but images and such go into a subdir). Run this
# with the html file as it's argument and it will spit to STDOUT a plain
# text version.

html_file = ARGV[0]
doc = Nokogiri::HTML(open(html_file))

# Grab all of the message containers
chat_messages = doc.search('div#chats div.hc-chat-row')

parsed_chat_messages = []

chat_messages.each do |message|
    message = {
        :timestamp => message.search('div.hc-chat-time').text.strip,
        :message => message.search('div.hc-chat-msg').text.strip,
        :name => message.search('div.hc-chat-from').text.strip
    }
    parsed_chat_messages << message
end

parsed_chat_messages.each do |message|
    puts "#{message[:timestamp]} #{message[:name]} -- #{message[:message]}"
end
