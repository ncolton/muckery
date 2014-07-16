#!/usr/bin/env ruby
# encoding: UTF-8
require 'nokogiri'

# Using HipChat's web interface, save the chat history as a web page (not
# an all-in-one file, but images and such go into a subdir). Run this
# with the html file as it's argument and it will spit to STDOUT a plain
# text version.

html_file = ARGV[0]
doc = Nokogiri::HTML(open(html_file))

chat_history_source = doc.search('div#chats div.chatBlock')
chat_history = []

chat_history_source.each do |message|
    message = {
        :timestamp => message.search('td.messageBlock').search('p.timeBlock').text.strip,
        :message => message.search('td.messageBlock').search('p.msgText').text.strip,
        :name => message.search('td.nameBlock').text.strip
    }
    chat_history << message
end

chat_history.each do |message|
    puts "#{message[:timestamp]} #{message[:name]} -- #{message[:message]}"
end
