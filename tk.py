#!/usr/bin/python
# -*- coding:utf-8 -*-
from Tkinter import * # Frame, Tk, 
import datetime
import time

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
    self.master.deiconify()   # 显示正常窗口的关键语句
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
    self.master.deiconify() # Tk

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
        root = Tk()
        app = Chat(master=root)
        # app.mainloop()
        self.master.destroy()

    def chatroom_list(self):
        print "hi!"

    def welcome(self):
        self.inputText = Label(self)
        self.inputText["text"] = "欢迎，请输入昵称:"
        self.inputText.pack(side="top")

        # 用于提示昵称冲突
        self.info_source = StringVar()
        self.info_source.set("")
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

        #self.hi_there = Button(self)
        #self.hi_there["text"] = "Enter",
        #self.hi_there["command"] = self.get_name
        #self.hi_there.pack(side="right")

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
        # app.master.title('python')
        # app.mainloop()
        self.master.destroy()

    def room_write(self):
        print "/write"
        #self.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Room(master=root, name="write")
        # app.mainloop()
        self.master.destroy()

    def room_pm(self):
        print "/pm"
        #elf.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Room(master=root, name="pm")
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
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.chat()
        self.master.title(name)
        position(self)

    def chat(self):
#窗口面板,用4个面板布局
        #self.frame = [Frame(), Frame(), Frame(), Frame()]
        self.frame_l_t = Frame(self)
        self.frame_l_m = Frame(self)
        self.frame_l_b = Frame(self)
        self.frame_r = Frame(self)
 
        self.QUIT = Button(self.frame_l_b)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["padx"] = 40
        self.QUIT["command"] =  self.quit
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

        #发送信息
        #显示消息Text右边的滚动条
        self.scrollbar = Scrollbar(self.frame_l_t)

        #显示消息Text，并绑定上面的滚动条
        self.chatText = Listbox(self.frame_l_t, width=70, height=18, yscrollcommand=self.scrollbar.set)
        for i in range(20):
            self.chatText.insert(END, 'hi\r\n')
        self.chatText.insert(END, 'HELLO')
        self.scrollbar.config(command=self.chatText.yview)
        # self.scrollbar(command=self.chatText.yview) 
        # AttributeError: Scrollbar instance has no __call__ method  ??
        self.scrollbar.pack(side="right", fill=Y)
        self.chatText.pack(side="left")
        self.frame_l_t.pack()


        self.source = StringVar()
        # self.source.set('your name')
        self.message_send = Entry(self.frame_l_m, textvariable=self.source)
        self.message_send["width"] = 70
        self.message_send.bind('<Return>', self.send_message)
        self.message_send.pack(fill=X) # , padx=25
        self.frame_l_m.pack()

    def online_people(self):
        print "/online"

    def send_message(self, event):
        self.chatText.insert(END, self.source.get())
        self.message_send.delete(0, END)

    def back_hall(self):
        print "hall"

# 创建一个顶层窗口，或者叫根窗口
root = Tk()
app = Welcome(master=root)

app.mainloop()

