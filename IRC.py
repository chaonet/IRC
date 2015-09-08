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
            try:
                meth(session, line)
            except TypeError:
                self.unknow(session, cmd)
                # print 22
        else:
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
        for session in self.sessions:
            session.push(line + '\r\n')

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
        print self.hall, 'hall at server'

    def handle_accept(self):
        conn,addr = self.accept()
        print conn, addr
        ChatSession(self, conn)
        # <socket._socketobject object at 0x10052d360> ('127.0.0.1', 62127)

class ChatSession(asynchat.async_chat, CommandHandler):
    
    def __init__(self, server, sock):
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        self.clint_name = ''
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
        session.send("welcome to IRC server!\r\n")
        session.send("Please log in use:\r\n/login name\r\n")
    
    def do_login(self, session, line):
        name = line.strip()
        if not name:
            session.send('Please enter a name.\r\n')
        elif name in self.server.users:
            session.send('The name "%s" is taken.\r\n' % name)
            session.send('Please try again.\r\n')
        else:
            session.clint_name = name
            self.server.users[session.clint_name] = session
            # print self.server.users, 1
            session.send('Welcome, %s\r\n' % session.clint_name)
            session.send("\r\nChatRoom list:\r\npython\r\nwrite\r\npm\r\n\r\nPlease log in use:\r\n/ChatRoom_name\r\n")

    def do_logout(self, session, line):
        del self.server.users[session.clint_name]
        Room.remove(self, session)
        Room.do_logout(self, session, line)

    def do_python(self):
        pass

    def do_write(self):
        pass

    def do_pm(self):
        pass

class Python(Room):
    pass

class Write(Room):
    pass

class Pm(Room):
    pass

if __name__ == '__main__':
    s = Server(port, host, hall_name)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass