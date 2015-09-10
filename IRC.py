# -*- coding: utf-8 -*-
import socket
import asyncore
import asynchat

host = '127.0.0.1'
port = 5000
hall_name = 'Learning'

class EndSession(Exception):pass  #用于产生异常，退出

class CommandHandler:

    def handle(self, session, line):
        if not line: return
        #print line
        parts = line.split(' ', 1)
        #print parts
        if parts[0][0] == '/':
            cmd = parts[0][1:]
            #print cmd
            try:
                line = parts[1].strip()
                #print line
            except IndexError:
                line = None
            meth = getattr(self, 'do_'+cmd, None)  # self ?？，和 房间绑定的？？
            print meth
            # <bound method Hall.do_login of <__main__.Hall instance at 0x1011105a8>>
            # <bound method Hall.do_python of <__main__.Hall instance at 0x1011105a8>>
            try:
                meth(session, line)
            except TypeError:
                self.unknow(session, cmd)
                print 22
        else:
            meth = getattr(self, 'do_broadcast', line)
            try:
                meth(session, line)
            except TypeError:
                self.unknow(session, line)

    def unknow(self, session, cmd):
        session.send('Unknow command: %s\r\n' % cmd)

class Room(CommandHandler):
    '''
    房间中的会话管理
    '''
    def __init__(self,server):
        self.sessions = []
        self.server = server

    def add(self,session):
        self.sessions.append(session)

    def remove(self,session):
        self.sessions.remove(session)

    def broadcast(self, session, line):
        print session,' session'
        print self.sessions,' self.sessions'
        for i in self.sessions:
            if i != session:
                i.push(line + '\r\n')

    def do_logout(self,session,line):
        raise EndSession

class Server(asyncore.dispatcher):
    
    def __init__(self, port, host, hall_name):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.sessions = []  # 保存服务器 当前的所有 client 会话列表
        self.users = {} # 用于比较是否有昵称冲突
        # hall = Hall(self)
        self.hall = Hall(self)   # server 启动便实例化 Hall ，作为 server 属性。同时 ，初始化hall，将 server 存为 hall 属性
        self.python = Python(self)
        self.write = Write(self)
        self.pm = Pm(self)
        print self.hall, 'hall at server'
        # <__main__.Hall instance at 0x1011105a8> hall at server

    def handle_accept(self):
        conn,addr = self.accept()
        print conn, addr
        # <socket._socketobject object at 0x10072c520> ('127.0.0.1', 53362)
        ChatSession(self, conn)

class ChatSession(asynchat.async_chat, CommandHandler):
    
    def __init__(self, server, sock):
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        self.client_name = ''
        # print self
        # <__main__.ChatSession connected 127.0.0.1:62127 at 0x10070c710>
        self.enter(server.hall)
        # self.enter(Hall(server))

    def enter(self, room):
        self.room = room
        room.add(self)  # 将新 session 添加到 hall 的 sessions 列表

    def collect_incoming_data(self, data):
        "缓存数据"
        self.data.append(data)
        # print data

    def found_terminator(self):
        line = ''.join(self.data) # 将所有发来的消息放入 line 中
        self.data = []
        # print line
        try:
            self.room.handle(self, line)  #对当前所在房间的方法进行查找，判断是否是命令
        except EndSession:
            self.handle_close()  #如果不是，调用退出房间的方法

    def handle_close(self):
        asynchat.async_chat.handle_close(self)

class Hall(Room):

    def add(self, session):
        self.sessions.append(session) # 将新的会话添加到 sessions 列表。sessions属性继承自 Room
        # print session.client_name
        if session.client_name == '':
            session.send("welcome to IRC server!\r\n")
            session.send("Please log in use:\r\n/login name\r\n")
        else:
            session.send("you now back to Hall\r\n")
    
    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.send('Please enter a name.\r\n')
        elif name in self.server.users:
            session.send('The name "%s" is taken.\r\n' % name)
            session.send('Please try again.\r\n')
        else:
            session.client_name = name
            self.server.users[session.client_name] = session
            # print self.server.users, 1
            session.send('Welcome, %s\r\n' % session.client_name)
            session.send("""\r\nChatRoom list:\r\npython\r\nwrite\r\npm
            \r\nPlease log in use:\r\n/ChatRoom_name\r\n""")

    def do_logout(self, session, line):
        del self.server.users[session.client_name]
        Room.remove(self, session)
        Room.do_logout(self, session, line)

    def do_python(self, session,line):
        print self.server.python
        # <__main__.Python instance at 0x1011105f0>
        session.enter(self.server.python)

    def do_write(self):
        pass

    def do_pm(self):
        pass

class Python(Room):

    def add(self, session):
        self.sessions.append(session) # 将新的会话添加到 sessions 列表。sessions属性继承自 Room
        session.send("welcome to ChatRoom 'Python'!\r\n")
        # Room.broadcast(self, session.client_name + ' has entered the room.') # wrong
        # self.broadcast(session.client_name + ' has entered the room.') # wrong
        # print self.broadcast
        # <bound method Python.broadcast of <__main__.Python instance at 0x1007105f0>>
        # print self
        # <__main__.Python instance at 0x1007105f0>
        self.broadcast(session, session.client_name + ' has entered the room.')

    def do_online(self, session, line):
        users = self.sessions
        # print users
        # [<__main__.ChatSession connected 127.0.0.1:53362 at 0x101110830>]
        if len(users) == 1: session.send('Nobody.\r\n')
        for i in users:
            if i != session:
                session.send(i.client_name + '\r\n')

    def do_back(self, session, line):
        session.enter(self.server.hall)
        # print Room
        # __main__.Room
        # print self
        # <__main__.Python instance at 0x1011105f0>
        # Room.remove(self, session)
        self.remove(session)

    def do_broadcast(self, session, line):
        self.broadcast(session, session.client_name + ': ' + line)

class Write(Room):
    pass

class Pm(Room):
    pass

if __name__ == '__main__':
    s = Server(port, host, hall_name)
    # print s
    # <__main__.Server listening 127.0.0.1:5000 at 0x100732dd0>
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass