#!/usr/bin/python
# -*- coding:utf-8 -*-

# from Tkinter import *
from telnetlib import *
import thread
import sys

from mtTkinter import *

host = "127.0.0.1"
port = 5000

server = Telnet(host, port)
# server = ''

def position(self):
    self.master.withdraw()  # 隐藏，不在界面显示部件，然后获取部件所在界面的尺寸
    self.screen_width = self.master.winfo_screenwidth()
    self.screen_height = self.master.winfo_screenheight()
    # print screen_width, screen_height
    # 1280 700

    #print root.winfo_width(), root.winfo_height()
    # 1 1

    self.master.resizable(False,False) # 固定尺寸，不可变

    #print root.winfo_width(), root.winfo_height()
    # 1 1

    self.master.update_idletasks()   # 显示正常窗口的关键语句
    self.master.deiconify()   # 重新显示
    # print root.winfo_width(), root.winfo_height()
    # 272 50

    self.master.withdraw() # TK
    self.master.geometry('%sx%s+%s+%s' %
            (
            self.master.winfo_width() ,
            self.master.winfo_height() ,
            (self.screen_width - self.master.winfo_width())/2,
            (self.screen_height - self.master.winfo_height())/2
            ))  # TK
    # print self.master.winfo_width(), self.master.winfo_height(), (self.screen_width/2 - self.winfo_width()), (self.screen_height/2 - self.winfo_height())
    # 11 * 11 +  面积+左上角顶点X轴坐标+Y轴坐标
    # 窗口宽度 * 窗口高度 * 窗口位置
    # 设置大小与位置
    self.master.deiconify()

    #self.master.mainloop() # 出现一次这个语句，就要 self.quit 一次……

class Welcome(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.welcome()
        self.master.title('IRC') # 要放在定位之前……
        position(self)

    def get_name(self, event):
        #self.master.destroy() # 关闭当前窗口
        name = self.source.get()
        server.write("/login " + name + "\r\n")
        s = server.read_until("More helps use: /help", 1)
        print s
        if "Please try again." in s:
            self.info["text"] = "The name is taken. Please change."
        else:
            root = Tk()
            app = Chat(master=root)
            self.master.destroy() # 销毁此组件 和 其子组件

    def welcome(self):
        self.inputText = Label(self)
        self.inputText["text"] = "欢迎，请输入昵称:"
        self.inputText.pack(side="top")

        self.info = Label(self)
        self.info["text"] = " "
        self.info.pack(side="top")
        
        self.source = StringVar()
        # self.source.set('your name')
        self.input_name = Entry(self, textvariable=self.source)
        self.input_name["width"] = 20
        self.input_name.bind('<Return>', self.get_name)
        self.input_name.pack(side="top", ipadx=25, padx=25)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack(side="left")

class Chat(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.chatroom()
        self.master.title('IRC')
        position(self)

    def room_python(self):
        print "/python"
        #self.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Room(master=root, name="python")
        app.startNewThread()
        # app.master.title('python')
        # app.mainloop()
        self.master.destroy()

    def room_write(self):
        print "/write"
        #self.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Room(master=root, name="write")
        app.startNewThread()
        # app.mainloop()
        self.master.destroy()

    def room_pm(self):
        print "/pm"
        #elf.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Room(master=root, name="pm")
        app.startNewThread()
        # app.mainloop()
        self.master.destroy()

    def chatroom(self):
        self.inputText = Label(self)
        self.inputText["text"] = "请选择聊天室进入:"
        self.inputText.pack(side="top")

        self.python = Button(self)
        self.python["text"] = "python"
        self.python["padx"] = 40
        self.python["command"] =  self.room_python
        self.python.pack(side="left")

        self.write = Button(self)
        self.write["text"] = "write"
        self.write["padx"] = 40
        self.write["command"] =  self.room_write
        self.write.pack(side="left")

        self.pm = Button(self)
        self.pm["text"] = "pm"
        self.pm["padx"] = 40
        self.pm["command"] =  self.room_pm
        self.pm.pack(side="left")

class Room(Frame):

    def __init__(self, master=None, name=None):
        Frame.__init__(self, master)
        server.write("/"+name+"\r\n")
        self.pack() # 用来管理和显示组件，默认 side = "top"

        self.frame_l_t = Frame(self)
        self.frame_l_m = Frame(self)
        self.frame_l_b = Frame(self)
        self.frame_r = Frame(self)

        self.QUIT = Button(self.frame_l_b)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["padx"] = 40
        self.QUIT["command"] =  self.offline
        self.QUIT.pack(side="left")
        
        self.back = Button(self.frame_l_b)
        self.back["text"] = "BACK"
        self.back["fg"]   = "red"
        self.back["padx"] = 40
        self.back["command"] =  self.back_hall
        self.back.pack(side="left")
        
        self.online = Button(self.frame_l_b)
        self.online["text"] = "online"
        self.online["padx"] = 40
        self.online["command"] = self.online_people
        self.online.pack(side="right")
        self.frame_l_b.pack()
        
        self.scrollbar = Scrollbar(self.frame_l_t)
        self.chatText = Listbox(self.frame_l_t, width=70, height=18, yscrollcommand=self.scrollbar.set)
        self.chatText.yview_moveto(1.0)
        self.scrollbar.config(command=self.chatText.yview)
        self.scrollbar.pack(side="right", fill=Y)
        self.chatText.pack(side="left")
        self.frame_l_t.pack()
        
        self.message_input = StringVar()
        self.message_send = Entry(self.frame_l_m, textvariable=self.message_input)
        self.message_send["width"] = 70
        self.message_send.bind('<Return>', self.send_message)
        self.message_send.pack(fill=X)
        self.frame_l_m.pack()


        self.master.title(name)
        position(self)

        self.chatText.insert(END, server.read_until("!"))


    def receiveMessage(self):
        socket = server.get_socket()
        while 1:
            clientMsg = socket.recv(4096)
            if not clientMsg:
                continue
            else:
                self.chatText.insert(END, clientMsg)
                self.chatText.yview_moveto(1.0)

    def startNewThread(self):
        thread.start_new_thread(self.receiveMessage, ())


    def online_people(self):
        # print "/online"
        server.write("/online" + "\r\n")

    def send_message(self, event):
        print "test"
        print self.message_input.get()
        send_mesg = self.message_input.get().strip(" ")
        print send_mesg
        if send_mesg:
            self.chatText.insert(END, send_mesg)
            server.write(send_mesg.encode("utf-8")+"\r\n")
            self.chatText.yview_moveto(1.0)
            self.message_send.delete(0, END)
        else:
            self.chatText.insert(END, "<不能发送空消息>")
            self.chatText.yview_moveto(1.0)
            self.message_send.delete(0, END)

    def back_hall(self):
        # print "hall"
        server.write("/back" + "\r\n")
        root = Tk()
        app = Chat(master=root)
        self.master.destroy()

    def offline(self):
        server.write("/logout\r\n")
        sys.exit()


# 创建一个根窗口

root = Tk()
app = Welcome(master=root)
# app = Connect(master=root)

root.mainloop()


"""
class Connect(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.connect_GUI()
        self.master.title('IRC') # 要放在定位之前……
        position(self)

    def connect_GUI(self):
        self.ip_port = Label(self)
        self.ip_port["text"] = "服务器地址         端口"
        self.ip_port.pack(side="top")

        self.server_ip = StringVar()
        self.server_ip.set(host)
        self.input_ip = Entry(self, textvariable=self.server_ip)
        self.input_ip["width"] = 5
        self.input_ip.pack(side="left", ipadx=30, padx=5)

        self.server_port = StringVar()
        self.server_port.set(port)
        self.input_port = Entry(self, textvariable=self.server_port)
        self.input_port["width"] = 1
        self.input_port.pack(side="left", ipadx=15, padx=5)

        self.QUIT = Button(self)
        self.QUIT["text"] = "enter"
        self.QUIT["fg"]   = "black"
        self.QUIT["command"] = self.connect
        self.QUIT.pack()

    def connect(self):
        global server
        self.ip = self.server_ip.get()
        self.port = self.server_port.get()

        server = Telnet(self.ip, self.port)
        
        root = Tk()
        app = Welcome(master=root)
        self.master.destroy()

"""
