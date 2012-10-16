#!/usr/bin/python
# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

class IrcBot(irc.IRCClient):
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        self.join('#minecraft')

    def joined(self, channel):
        """This will get called when the bot joins the channel."""

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        #print 'Receve ', channel, ' ', msg
        #self.chat.irc_message_receve(channel, user, msg)
        #if user == 'kolkо':
        #    if msg.startswith('!!'):
        #        self.pp.transport.write("%s\n"%(msg[2:],))
        if channel == self.channel:
            print 'receved', msg
            self.pp.transport.write("say <%s>: %s\n"%(user,msg))


    # For fun, override the method that determines how a nickname is changed on
    # collisions. The default method appends an underscore.
    def alterCollidedNick(self, nickname):
        """
        Generate an altered version of a nickname that caused a collision in an
        effort to create an unused related name for subsequent registration.
        """
        return nickname + '^'
    
    ##new##
    
#    def userRenamed(self, oldname, newname):
#        self.chat.irc_nick_change(oldname, newname)
    
#    def userKicked(self, kickee, channel, kicker, message):    
#        self.chat.irc_user_kick(kickee, channel, kicker, message)
        
#    def userQuit(self, user, quitMessage):
#        self.chat.irc_user_part(self.chat.irc_channel, user, quitMessage) # self.chat.irc_channel - cheat :(
        
#    def userLeft(self, user, channel):
#        self.chat.irc_user_part(channel, user)
        
#    def userJoined(self, user, channel):
#        self.chat.irc_user_join(channel, user)
        
#    def nickChanged(self, nick):
#        self.nickname = nick
#        self.chat.irc_nick = nick
        
#    def kickedFrom(self, channel, kicker, message):
#        self.chat.irc_user_kick(self.nickname, channel, kicker, message)
        
#    def action(self, user, channel, data):
#        self.chat.irc_action(user, channel, data)
        
#    def topicUpdated(self, user, channel, newTopic):
#        self.chat.irc_topic_changed(user, channel, newTopic)


class IrcBotFactory(protocol.ClientFactory):

    def __init__(self, channel, nickname, pp):
        self.protocol = IrcBot
        self.nickname = nickname
#        self.chat = chat
#        chat.irc_nick = nickname
        self.channel = channel
        self.connected = 0
        self.pp = pp
        
    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.nickname = self.nickname
#        proto.chat = self.chat
        proto.factory = self
        proto.channel = self.channel
        proto.pp = self.pp
        self.protocol_ = proto
        return proto
        
    def startedConnecting(self, connector):        #WROOOOOOOOOOOONG!
        print 'Irc connect starting..'
        self.connected = 1
        
    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        print 'Irc connection lost: ', reason
        self.connected = 0
        reactor.callLater(10.0, connector.connect)

    def clientConnectionFailed(self, connector, reason):
        print "irc connection failed:", reason
        #reactor.stop()
        self.connected = 0
        reactor.callLater(10.0, connector.connect)
        
        

