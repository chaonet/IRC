# -*- coding: utf-8 -*-
import socket
import asyncore
import asynchat

host = '127.0.0.1'
port = 5000
hall_name = 'Learning'

class Command(object):
    pass

class Server(asyncore.dispatcher):
    
    def __init__(self, port, host, hall_name):
    	asyncore.dispatcher.__init__(self)
    	self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    	self.set_reuse_addr()
    	self.bind((host, port))
    	self.listen(5)

    def handle_accept(self):
    	conn,addr = self.accept()
    	print "Connected from", conn

class Hall(Command):
    pass

class ChatSession(object):
    pass

if __name__ == '__main__':
    s = Server(port, host, hall_name)
    asyncore.loop()