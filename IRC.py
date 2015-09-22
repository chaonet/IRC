# -*- coding: utf-8 -*-
import socket
import asyncore
import asynchat

host = '127.0.0.1'
port = 5000
# hall_name = 'Learning'

class EndSession(Exception):pass  #用于产生异常，退出

class CommandHandler:
    '''
    消息处理。
    根据用户发来的消息进行判断，并调用对应的实例方法。
    分为'/'开头的命令，和普通的消息。
    '''
    def handle(self, session, line):
        '''
        尝试对消息进行拆分、判断
        '''
        if not line: return
        #print line
        parts = line.split(' ', 1)
        #print parts
        if parts[0][0] == '/': # 检查是否命令，命令格式：/cmd
            cmd = parts[0][1:]
            #print cmd
            try:
                line = parts[1].strip()
                #print line
            except IndexError:
                line = None
            meth = getattr(self, 'do_'+cmd, None)  # 查看用户所在的房间是否有该属性/方法。self ，和 房间绑定
            # print meth
            # <bound method Hall.do_login of <__main__.Hall instance at 0x1011105a8>>
            # <bound method Hall.do_python of <__main__.Hall instance at 0x1011105a8>>
            try:
                meth(session, line)
            except TypeError:
                self.unknow(session, cmd)
        else:   # 对于普通的聊天信息，默认直接调用 'do_broadcast' 方法广播给房间内其他人
            meth = getattr(self, 'do_broadcast', line)
            try:
                meth(session, line)
            except TypeError:
                self.unknow(session, line)

    def unknow(self, session, cmd):
        '''
        当找不到相应的命令时，进行提示
        '''
        session.send('Unknow command: %s\r\n' % cmd)

class Room(CommandHandler):
    '''
    房间的会话管理，继承了 'CommandHandler' 类
    '''
    def __init__(self, server, room_name):
        '''
        初始化房间，每个房间保存当前用户的会话列表，服务器实例，房间名称
        '''
        self.sessions = []
        self.server = server
        self.room_name = room_name

    def add(self,session):
        self.sessions.append(session)

    def remove(self,session):
        self.sessions.remove(session)

    def broadcast(self, session, line):
        '''
        广播消息给房间内，除自己外的所有人
        '''
        # print session,' session'
        # print self.sessions,' self.sessions'
        for i in self.sessions:
            if i != session:
                i.send(line + '\r\n')

    def do_logout(self,session,line):
        raise EndSession

class Server(asyncore.dispatcher):
    '''
    服务器类
    '''
    def __init__(self, port, host):
        '''
        初始化服务器，开始侦听用户的服务请求。
        以字典方式保存所有用户的 client_name 和 session 映射信息，避免昵称冲突
        初始化 Hall 以及 三个聊天室
        '''
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.users = {} # 用于比较是否有昵称冲突
        self.hall = Hall(self, 'Hall')   # server 启动便实例化 Hall ，作为 server 属性。同时 ，初始化hall，将 server 存为 hall 属性
        self.python = ChatRoom(self, 'python')
        self.write = ChatRoom(self, 'write')
        self.pm = ChatRoom(self, 'pm')
        # print self.hall, 'hall at server'
        # <__main__.Hall instance at 0x1011105a8> hall at server

    def handle_accept(self):
        '''
        接受用户的接入请求，为每个用户分配一个 socket 对象，也是与用户通信的接口
        为每一个用户初始化一个ChatSession
        '''
        conn,addr = self.accept()
        # print conn, addr
        # <socket._socketobject object at 0x10072c520> ('127.0.0.1', 53362)
        ChatSession(self, conn)

class ChatSession(asynchat.async_chat):
    '''
    处理与单个用户的消息，发送、接收消息。
    '''
    def __init__(self, server, sock):
        asynchat.async_chat.__init__(self, sock)
        self.set_terminator('\r\n')
        self.data = []
        self.client_name = '' # 保存每个用户的用户名
        # print self
        # <__main__.ChatSession connected 127.0.0.1:62127 at 0x10070c710>
        self.enter(server.hall) # 调用 'enter' 方法，更改用户所在的房间，并将用户的会话添加到房间的session列表
        # self.enter(Hall(server))

    def enter(self, room):
        '''
        更改用户所在的房间，并将 用户的会话 添加到 房间的session列表
        '''
        self.room = room
        room.add(self)  # 将新 session 添加到 hall 的 sessions 列表

    def collect_incoming_data(self, data):
        '''
        缓存从用户收到的数据
        '''
        self.data.append(data)
        # print data

    def found_terminator(self):
        '''
        将 从用户接收到的消息 发给 房间的消息处理函数 进行处理
        '''
        line = ''.join(self.data) # 将所有发来的消息放入 line 中
        self.data = []
        print line
        try:
            self.room.handle(self, line)  #对当前所在房间的方法进行查找，判断是否是命令
        except EndSession:
            self.handle_close()  #如果不是，调用退出房间的方法

    def handle_close(self):
        asynchat.async_chat.handle_close(self)

class Hall(Room):
    '''
    大厅，登陆到大厅后，选择聊天室
    '''
    def add(self, session):
        '''
        将 新用户的会话 添加到 房间的用户列表
        如果是初次登陆，要求输入昵称
        如果是从聊天室返回大厅的用户，简单给出提示信息
        '''
        self.sessions.append(session) # 将新的会话添加到 sessions 列表。sessions属性继承自 Room
        if session.client_name == '':
            session.send("welcome to IRC server!\r\n")
            session.send("Please log in use:\r\n/login name\r\n")
        else:
            session.send("you now back to Hall\r\n")
    
    def do_login(self, session, line):
        '''
        对用户输入的昵称处理。
        给出帮助信息。
        '''
        name = line.strip()
        if not name:
            session.send('Please enter a name.\r\n')
        elif name in self.server.users: # 如果输入的昵称已经存在，要求重新选择
            session.send('The name "%s" is taken.\r\n' % name)
            session.send('Please try again.\r\n')
        else:
            session.client_name = name  # 将昵称作为 用户自身属性 进行保存
            self.server.users[session.client_name] = session # 在服务器的字典中添加新用户的 昵称：会话 信息
            # print self.server.users, 1
            session.send('Welcome, %s\r\n' % session.client_name)
            session.send("""
            \r\nChatRoom list:\r\npython\r\nwrite\r\npm
            \r\nPlease log in use:\r\n/ChatRoom_name
            \r\nMore helps use: /help\r\n""")

    def do_logout(self, session, line):
        '''
        用户退出连接
        '''
        del self.server.users[session.client_name] # 从服务器的字典中删除 键：值 对
        Room.remove(self, session)    # 从房间的用户会话列表删除
        Room.do_logout(self, session, line)  # 利用错误消息中断连接

    def do_python(self, session, line):
        '''
        进入聊天室 python
        '''
        # print self.server.python
        # <__main__.Python instance at 0x1011105f0>
        session.enter(self.server.python)

    def do_write(self, session, line):
        session.enter(self.server.write)

    def do_pm(self, session, line):
        session.enter(self.server.pm)

    def do_help(self, session, line):
        '''
        发送帮助信息
        '''
        session.send(
        """
        \r\n/python enter ChatRoom 'python'
        \r\n/write  enter ChatRoom 'write'
        \r\n/pm     enter ChatRoom 'pm'
        \r\n/logout exit
        \r\n/help   get helps
        \r\n""")

class ChatRoom(Room):
    '''
    聊天室类
    '''
    def add(self, session):
        '''
        添加用户到聊天室
        并将 用户进入的消息 广播给其他人
        '''
        self.sessions.append(session) # 将新的会话添加到 sessions 列表。sessions属性继承自 Room
        session.send("welcome to ChatRoom %s!\r\n" % self.room_name)
        # Room.broadcast(self, session.client_name + ' has entered the room.') # wrong
        # self.broadcast(session.client_name + ' has entered the room.') # wrong
        # print self.broadcast
        # <bound method Python.broadcast of <__main__.Python instance at 0x1007105f0>>
        # print self
        # <__main__.Python instance at 0x1007105f0>
        self.broadcast(session, session.client_name + ' has entered the room.')

    def do_online(self, session, line):
        '''
        查看房间内有哪些其他用户
        '''
        users = self.sessions
        # print users
        # [<__main__.ChatSession connected 127.0.0.1:53362 at 0x101110830>]
        if len(users) == 1: session.send('Nobody.\r\n')
        for i in users:
            if i != session:
                session.send(i.client_name + '\r\n')

    def do_back(self, session, line):
        '''
        退回到大厅
        '''
        session.enter(self.server.hall)
        # print Room
        # __main__.Room
        # print self
        # <__main__.Python instance at 0x1011105f0>
        # Room.remove(self, session)
        self.remove(session)

    def do_broadcast(self, session, line):
        '''
        广播消息给房间内其他所有人
        '''
        self.broadcast(session, session.client_name + ': ' + line)

    def do_help(self, session, line):
        session.send(
        """
        \r\n/online  other users in python
        \r\n/back    back to hall
        \r\n/help    get helps
        \r\n""")

if __name__ == '__main__':
    s = Server(port, host)
    # print s
    # <__main__.Server listening 127.0.0.1:5000 at 0x100732dd0>
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass