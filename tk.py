#!/usr/bin/python
# -*- coding:utf-8 -*-
from Tkinter import *
import datetime
import time

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.welcome()

    def welcome(self):
        self.inputText = Label(self)
        self.inputText["text"] = "欢迎，请输入昵称:"
        self.inputText.pack(side="top")
        
        self.source = StringVar()
        # self.source.set('your name')
        self.input_name = Entry(self, textvariable=self.source)
        self.input_name["width"] = 20
        self.input_name.bind('<Key-Return>', self.get_name)
        self.input_name.pack(side="top", ipadx=25, padx=25)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack(side="left")

        self.hi_there = Button(self)
        self.hi_there["text"] = "Enter",
        self.hi_there["command"] = self.get_name
        self.hi_there.pack(side="right")

    def get_name(self, event):
        print "/login " + self.source.get()
        self.master.destroy()
        # self.master.destroy()
        # print self
        root = Tk()
        app = Application_1(master=root)
        app.master.title('IRC')
        # app.master.maxsize(1000, 400)
        app.mainloop()

    def chatroom_list(self):
        print "hi!"

class Application_1(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.chatroom()

    def room_python(self):
        print "/python"
        self.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Application_2(master=root)
        app.master.title('python')
        # app.master.maxsize(1000, 400)
        app.mainloop()

    def room_write(self):
        print "/write"
        self.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Application_2(master=root)
        app.master.title('write')
        # app.master.maxsize(1000, 400)
        app.mainloop()

    def room_pm(self):
        print "/pm"
        self.master.destroy() # 关闭当前窗口
        root = Tk()
        app = Application_2(master=root)
        app.master.title('pm')
        # app.master.maxsize(1000, 400)
        app.mainloop()

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

class Application_2(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.chat()

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
        self.back["command"] =  self.quit
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

# 创建一个顶层窗口，或者叫根窗口
root = Tk()
# print root, 1
# .
app = Application(master=root)
# print app, 2
app.master.title('IRC')

root.withdraw()    #hide window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight() - 100    #under windows, taskbar may lie under the screen
root.resizable(False,False)

root.update_idletasks()
root.deiconify()    #now window size was calculated
root.withdraw()     #hide window again
root.geometry('%sx%s+%s+%s' % \
    (root.winfo_width() + 10, root.winfo_height() + 10, \
        (screen_width - root.winfo_width())/2, \
        (screen_height - root.winfo_height())/2) )    #center window on desktop
root.deiconify()

# app.master.maxsize(1000, 400)

# 进入窗体的主循环
app.mainloop()
