#!/usr/bin/python
# -*- coding:utf-8 -*-
from Tkinter import *

class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack() # 用来管理和显示组件，默认 side = "top"
        self.welcome()
        self.source = ''

    def welcome(self):
        self.inputText = Label(self)
        self.inputText["text"] = "欢迎，请输入昵称:"
        self.inputText.pack(side="top")
         
        self.source = StringVar()
        # self.source.set('your name')
        self.input_name = Entry(self, textvariable=self.source)
        self.input_name["width"] = 20
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

    def get_name(self):
        print self.input_name.get()

    def chatroom_list(self):
        print "hi!"

# 创建一个顶层窗口，或者叫根窗口
root = Tk()
app = Application(master=root)
app.master.title('IRC')
app.master.maxsize(1000, 400)

# 进入窗体的主循环
app.mainloop()
root.destroy()