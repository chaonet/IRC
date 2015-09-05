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
        ChatSession(conn)

class ChatSession(asynchat.async_chat):
    
    def __init__(self, sock):
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        print "welcome to IRC server"

    def collect_incoming_data(self, data):
        "缓存数据"
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        print line

class Hall(Command):
    pass

if __name__ == '__main__':
    s = Server(port, host, hall_name)
    asyncore.loop()