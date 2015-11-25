#!/usr/bin/python

# (c) Copyright 2015 Nathan Krantz-Fire (a.k.a zippynk). Some rights reserved.
# https://github.com/zippynk

# https://github.com/zippynk/DumbIRC



#      This Source Code Form is subject to the
#            terms of the Mozilla Public License, v.
#                  2.0. If a copy of the MPL was not
#                        distributed with this file, You can
#                              obtain one at
#                                    http://mozilla.org/MPL/2.0/.
#                                       What in the world is going
#                                          on with my license notice?
#                                               Ugh, Vim.
from __future__ import print_function
from pyrcb.pyrcb import IRCBot
from datetime import datetime
import sys
import os
from bottle import *

def atleast2digitize(x):
    return x if len(str(x)) > 1 else int("0" + str(x))

messages = []

class LogBot(IRCBot):
    def on_message(self, message, nickname, channel, is_query):
        if channel == self.mainChannel:
            self.log("{0}:{1} &lt;{2}&gt; {3}".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nickname,message))

    def on_join(self, nickname, channel):
        if channel == self.mainChannel:
            self.log("{0}:{1} -!- {2} has joined {3}".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nickname,channel))
   
    def on_notice(self,message,nickname,channel,is_query): 
        if channel == self.mainChannel:
            self.log("{0}:{1} -{2}:{3}- {4}".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nickname,target,message))
        
         
    def on_quit(self, nickname, message):
        self.log("{0}:{1} -!- {2} has quit [{3}]".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nickname,message))

    def on_part(self, nickname, channel, message):
        if channel == self.mainChannel:
            self.log("{0}:{1} -!- {2} has parted {3} [{4}]".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nickname,channel,message))

    def on_kick(self, nickname, channel, target, message):
        if channel == self.mainChannel:
            self.log("{0}:{1} -!- {2} has been kicked from {3} by {4} [{5}]".format(datetime.now().hour,atleast2digitize(datetime.now().minute),target,nickname,channel,message))

    def on_nick(self,nickname,new_nickname):
        self.log("{0}:{1} -!- {2} is now known as {3}".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nickname,new_nickname))
    
    def on_names(self,channel,names):
        self.log("{0}:{1} People in {2}: {3}".format(datetime.now().hour,atleast2digitize(datetime.now().minute),channel,", ".join(names)))

    def log(self,message):
        messages.append(message)

    def logFile(self):
        return self.logFilePrefix + "_" + str(datetime.now().year) + "_" + str(datetime.now().month) + "_" + str(datetime.now().day)

@route("/")
def homePage():
    return "<html><head><title>IRC</title></head><body><p>" + "</p><p>".join(messages) + "</p><form action='send' method='POST'><textarea name='message'></textarea><br/><input type='submit' name='submit' value='Send'></form></body></html>"

@post("/send")
def sendMessage():
    message = request.forms.get("message")
    bot.send(bot.mainChannel,message)
    bot.log("{0}:{1} &lt;{2}&gt; {3}".format(datetime.now().hour,atleast2digitize(datetime.now().minute),nick,message))

    redirect("/")

def main():
    global bot
    bot = LogBot(debug_print=True)
    bot.mainChannel = sys.argv[4]
    global port
    port = sys.argv[5]
    global nick
    nick = sys.argv[3]
    bot.connect(sys.argv[1], int(sys.argv[2]))
    if len(sys.argv) > 6:
        bot.password(sys.argv[6])
    bot.register(nick)
    bot.join(bot.mainChannel)
    bot.listen_async()
    run(host="0.0.0.0",port=port,debug=False)
    print("Disconnected from server.")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python3 DumbIRC.py <server> <port> <nick> <channel> <port to host web server> <password (optional)>")
        exit(1)
    main()
