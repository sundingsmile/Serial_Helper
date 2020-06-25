from serial import Serial
import time
import threading
import multiprocessing


# def test():
#     ser = Serial('com13', 115200, timeout=1)
#     while 1:
#         print(123)
#         ser.write('abc'.encode())
#         time.sleep(1)
#         print(ser.read_until())
#         # print('线程id')
#
# b = threading.Thread(target=test)
# b.run()
# time.sleep(5)
# print(5,b.is_alive())
# time.sleep(10)
# print(b.is_alive())

# if __name__ == '__main__':
#     a = multiprocessing.Process(target=test)
#     a.start()
#     time.sleep(20)
#     # print('我要关闭进程了')
#     a.kill()
#
#     time.sleep(10)
#     print( a.is_alive(),'执行了')

# class test(threading.Thread):
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.ser = Serial('com13', 115200, timeout=1)
#         self.__running = threading.Event()
#         self.__running.set()
#
#     def run(self):
#         while self.__running.isSet():
#             print(self.__running.isSet())
#             self.ser.write('abc'.encode())
#             time.sleep(1)
#             print(self.ser.read_until())
#
#     def stop(self):
#         self.__running.clear()
#
#     # def start(self):
#     #     b = threading.Thread(target=self.run)
#     #     b.start()
#
# cc = test()
# cc.start()
# time.sleep(10)
# print(cc.is_alive(),'first')
# cc.stop()
# time.sleep(2)
# print(cc.is_alive(),'end')
#
# import tkinter as tk
#
# root = tk.Tk()
#
# text = tk.Text(root, width=20, height=5)
# text.pack()
#
# s = "I love Python!"
#
#
# text.insert('end', s)
# text.config(state=tk.DISABLED)

# def show():
#     print("哎呀，我被点了一下~")
#
#
# b1 = tk.Button(text, text="点我点我", command=show)
# text.window_create("end", window=b1)

# root.mainloop()

# from tkinter import *
#
# master = Tk()

# scrollbar = Scrollbar(master)
# scrollbar.pack(side=RIGHT, fill=Y)
#
# listbox = Listbox(master, yscrollcommand=scrollbar.set)
# for i in range(1000):
#     listbox.insert(END, str(i))
# # listbox.pack(side=LEFT, fill=BOTH)
# listbox.grid()
# scrollbar.config(command=listbox.yview)
#
# mainloop()
#

# a = Message(master,{'1':'hello'})
# a.pack()
#
# mainloop()

# from tkinter import messagebox
# from tkinter import *
#
# a = messagebox.showerror('你好','吃饭了吗')
#
# mainloop()

from tkinter import *


# def call_back(event):
#     print(event.char)  # 按哪个键，在console中打印
#
#
# def main():
#     root = Tk()
#
#     # 创建一个框架，在这个框架中响应事件
# #     frame = Frame(root,
# #                   width=200, height=200,
# #                   background='green')
# #
# #
# #     frame.pack()
# #     text = Text()
# #     text.bind("<Key>", call_back)
# #     text.pack()
# #     # 当前框架被选中，意思是键盘触发，只对这个框架有效
# #     frame.focus_set()
# #
# #     mainloop()

import time
def main():
    t = Test()
    t.run()

class Test():
    def __init__(self):
        root = Tk()
        self.text = Text()
        self.text.bind("<Key>", self.callback)
        self.text.pack()

    def callback(self,event):
        if event.char not in 'abcdefABCDEF0123456789' + :
            ss = self.text.get(1.0,'end')
            self.text.insert('end',ss)
        else:
            # s = self.text.search(self.text.get(1.0,'end'),1.0,regexp='j')
            # print(self.text.get(1.0, 'end'))
            # print(s)
            self.text.delete('insert')



    def run(self):
        mainloop()
if __name__ == '__main__':
    main()


