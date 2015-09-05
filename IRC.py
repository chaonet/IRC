# -*- coding: utf-8 -*-
import socket
import asyncore
import asynchat

host = 127.0.0.1
port = 5000
hall_name = 'Learning'

class Command(object):
    pass

class Server(asyncore.dispatcher):
    pass

class Hall(Command):
    pass

class ChatSession(object):
    pass

if __name__ = '__main__':
    s = Server(port, host, hall_name)
    asyncore.loop()