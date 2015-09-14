#!/usr/bin/python
# -*- coding:utf-8 -*-
from Tkinter import *

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
        print "/login " + self.source.get()
        self.master.destroy() # 关闭当前窗口
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

    def room_write(self):
        print "/write"

    def room_pm(self):
        print "/pm"

    def chatroom(self):
        self.inputText = Label(self)
        self.inputText["text"] = "请选择聊天室进入:"
        self.inputText.pack(side="top")

        self.python = Button(self)
        self.python["text"] = "python"
        self.python["command"] =  self.room_python
        self.python.pack(side="left")

        self.write = Button(self)
        self.write["text"] = "write"
        self.write["command"] =  self.room_write
        self.write.pack(side="left")

        self.pm = Button(self)
        self.pm["text"] = "pm"
        self.pm["command"] =  self.room_pm
        self.pm.pack(side="left")
"""
        self.name = StringVar()

        self.name.set("chat")
        self.python = Radiobutton(self, text="python",variable=self.name, value="python", command=self.room_name())
        self.python.pack(anchor = W)

        self.write = Radiobutton(self, text="write",variable=self.name, value="write", command=self.room_name())
        self.write.pack(anchor = W)

        self.pm = Radiobutton(self, text="pm",variable=self.name, value="pm", command=self.room_name())
        self.pm.pack(anchor = W)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack(side="left")
"""


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
root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10, (screen_width - root.winfo_width())/2, (screen_height - root.winfo_height())/2) )    #center window on desktop
root.deiconify()

# app.master.maxsize(1000, 400)

# 进入窗体的主循环
app.mainloop()
