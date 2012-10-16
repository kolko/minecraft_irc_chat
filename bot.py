#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.internet import protocol
from twisted.internet import reactor
import re

class MyPP(protocol.ProcessProtocol):
    
    def __init__(self):
        self.players = []
        self.data = ''
    
    def connectionMade(self):
        print "connectionMade!"
#        for i in range(self.verses):
#            self.transport.write("Aleph-null bottles of beer on the wall,\n" +
#                                 "Aleph-null bottles of beer,\n" +
#                                 "Take one down and pass it around,\n" +
#                                 "Aleph-null bottles of beer on the wall.\n")
#        self.transport.closeStdin() # tell them we're done
    def outReceived(self, data):
        print "outReceived! with %d bytes!" % len(data)        
        for str in data.splitlines():
            self.input(str)
#        self.data = self.data + data
#        if self.irc_proto:
#            if self.irc_proto.protocol_:
#                self.irc_proto.protocol_.msg('#minecraftwikichanges', data[:200])
                
    def errReceived(self, data):
        print "errReceived! with %d bytes!" % len(data)
	for str in data.splitlines():
            self.input(str)
#        if self.irc_proto:
#            if self.irc_proto.protocol_:
#                self.irc_proto.protocol_.msg('#minecraftwikichanges', data[:200])
#                print data[:200].decode('utf-16')         
   
    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"
    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"
        # now is the time to examine what they wrote
        print "I saw them write:", self.data
        
        #(dummy, lines, words, chars, file) = re.split(r'\s+', self.data)
        #print "I saw %s lines" % lines
    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."
    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)
    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        reactor.stop()
        
        
############
#new proto
############
    def input(self, data):
        warn = re.compile(r'^(?P<datetime>[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[WARNING\] (?P<text>.*)$')
        m = warn.search(data)
        if m:
            self.input_warn(m.group('datetime'), m.group('text'))
            return
        info = re.compile(r'^(?P<datetime>[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}) \[INFO\] (?P<text>.*)$')
        m = info.search(data)
        if m:
            self.input_info(m.group('datetime'), m.group('text'))
            return
        else:
            print 'not parsed str: %s'%data

    def input_warn(self, datetime, text):
        print 'input_warning'
        
    def input_info(self, datetime, text):
        print 'input_info'
        join = re.compile(r'^(?P<nick>[^ ]+) \[(?P<claddr>[^\]]+)\] logged in with entity id (?P<clid>\d+) at \((?P<coords>.*)\)$')
        m = join.search(text)
        if m:
            self.input_join(datetime, m.group('nick'), m.group('claddr'), m.group('clid'), m.group('coords'))
            return
        part = re.compile(r'^(?P<nick>[^ ]+) lost connection: (?P<reason>.*)$')
        m = part.search(text)
        if m:
            self.input_part(datetime, m.group('nick'), m.group('reason'))
            return
        chat = re.compile(r'^<(?P<nick>[^ ]+)> (?P<msg>.*)$')
        m = chat.search(text)
        if m:
            if m.group('nick') in self.players:
                self.input_chat(datetime, m.group('nick'), m.group('msg'))
                return
        #Disconnecting /31.207.155.40:50486: Took too long to log in
        user_disconnect = re.compile(r'^Disconnecting (?P<user>[^ ]+): (?P<msg>.*)$')
        m = user_disconnect.search(text)
        if m:
            self.input_user_disconnect(datetime, m.group('user'), m.group('msg'))
            return
        print 'not parsed str in info: %s'%text
            
    def input_join(self, datetime, nick, claddr, clid, coords):
        print 'client join'
        if nick not in self.players:
            self.players.append(nick)
        self.output_send('client join %s'%(nick,))
        #self.output_send('client join %s, %s'%(nick, claddr))
        
    def input_part(self, datetime, nick, reason):
        print 'client part'  
        if nick in self.players:
            self.players.remove(nick)
        self.output_send('client %s gone: %s'%(nick, reason))
        
    def input_chat(self, datetime, nick, msg):
        print 'client chat'
        self.output_send('<%s>: %s'%(nick,msg))
        
    def input_user_disconnect(self, datetime, user, msg):
        print 'client disconnect'
        self.output_send('User %s disconnect: %s'%(user,msg))
        
    def output_send(self, data):
        if self.irc_proto:
            if self.irc_proto.protocol_:
                self.irc_proto.protocol_.msg('#minecraft', data[:200])