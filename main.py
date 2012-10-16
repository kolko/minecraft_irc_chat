#!/usr/bin/python
# -*- coding: utf-8 -*-

import irc, bot
from twisted.internet import reactor#, protocol
import sys

irc_server = 'irc.tsure.ru'
irc_server_port = 6666
irc_nick = 'bot'
irc_channel = '#minecraft'

pp = bot.MyPP()
reactor.spawnProcess(pp, "java", ["java", "-Xmx1024M", "-Xms1024M", "-jar", "minecraft_server.jar", "nogui"], {'LANG':'ru_RU.UTF-8'})
#reactor.run()
print sys.getdefaultencoding()
#chat_module = chat.chat(irc_channel)

irc_module = irc.IrcBotFactory(irc_channel, irc_nick, pp)
pp.irc_proto = irc_module

#delayer_module = delayer.delayer(irc_module, None)

#icq_module = icq.oscarAuth(chat_module, icq_uin, icq_pass, icq_server, icq_server_port, delayer_module)

#chat_module.delayer = delayer_module
reactor.connectTCP(irc_server, irc_server_port, irc_module)
reactor.run()