from tkinter import Tk,Text,Scrollbar,DISABLED,NORMAL,Y,RIGHT,END,messagebox,IntVar
from tkinter.ttk import Combobox,Label,LabelFrame,Button,Radiobutton
from serial import Serial
from serial.tools import list_ports
from threading import Thread
import time,threading,win32clipboard

def main():
    a = Assist_Serial_Port()
    a.run()

class Assist_Serial_Port():
    def __init__(self):
        self.BTL = [110, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 38400, 56000, 57600, 115200, 128000, 256000]  # 波特率下拉列表框内容
        self.JYW = ['NONE', 'ODD', 'EVEN', 'MARK', 'SPACE']  # 校验位下拉列表框内容
        self.SJW = [5, 6, 7, 8]  # 数据位下拉列表内容
        self.TZW = [1, 1.5, 2]  # 停止位下拉列表内容
        self.CKXX = self.read_serial_info()
        self.PZMC = ['串口号','波特率','校验位','数据位','停止位']
        self.serial_res_hex_bzw = False  # 接收数据框内容显示hex标志位
        self.serial_sen_hex_bzw = False  # 发送数据框内容显示hex标志位
        self.radiobutton_sen_ascii_click_count = 1  # 设置发送ASCII单选框点击次数为0
        self.radiobutton_sen_hex_click_count = 0  # 设置发送HEX单选框点击次数为0

        self.root = Tk(className='串口调试助手')  # 创建一个主窗体，并命名为‘串口调试助手’
        self.root.protocol('WM_DELETE_WINDOW',self.close_window)  # 实现点击窗口关闭按钮，调用self.close_window方法，关闭已经打开的串口，销毁窗口
        self.root.geometry('630x580')  # 设置窗体大小
        self.root.minsize(width=630, height=435)  # 这两句语言限制窗口不能随意变化
        self.root.maxsize(width=630, height=435)

        self.lf = LabelFrame(self.root, text='串口设置')  # 创建标签容器，并且命名为‘串口设置’
        self.lf.grid(padx=8, pady=10,ipadx=3, ipady=5,row=1,column=1,sticky='n')  # 设置标签容器在窗口中的位置

        self.text_res_con = LabelFrame(master=self.root,text='接收设置')  # 创建标签容器，并命名为接收设置
        self.text_res_con.grid(row=1,column=1,sticky='s')  # 设置标签容器在窗口中的位置

        self.text_sen_con = LabelFrame(master=self.root,text='发送设置')  # 创建标签容器，并命名为接收设置
        self.text_sen_con.grid(padx=8, pady=10,row=2,column=1,sticky='nesw')  # 设置标签容器在窗口中的位置

        self.data_rec = LabelFrame(self.root, text='数据日志')  # 创建标签容器，并且命名为‘数据日志’
        self.data_rec.grid(ipadx=3, ipady=5,row=1, column=2, sticky='e')  # 设置标签容器在窗口中的位置

        self.y_scroll = Scrollbar(self.data_rec)  # 创建接收文本框的Y轴下拉框
        self.y_scroll.pack(side=RIGHT,fill=Y)  # 确定位置

        self.result_text = Text(master=self.data_rec,height=22,width=66,yscrollcommand=self.y_scroll.set) # 创建一个多文本组件，用来显示接收的串口信息，并且配置关联滚轴
        self.result_text.pack(side=RIGHT,fill=Y)  # 设置多文本组件在窗口中的位置
        self.y_scroll.config(command=self.result_text.yview)  # 让文本框和滚轴关联起来

        self.data_sen = LabelFrame(self.root, text='数据发送')  # 创建标签容器，并且命名为‘数据日志’
        self.data_sen.grid(ipadx=3, ipady=5,row=2, column=2, sticky='w')  # 设置标签容器在窗口中的位置

        self.send_text = Text(master=self.data_sen,height=6,width=60)  # 创建一个发送文本框
        self.send_text.grid(row=1,column=1,sticky='n')  # 设置标签容器在窗口中的位置

        self.button_send = Button(self.data_sen,text='发送消息',command=self.button_send_serial_click,width=7)  # 创建一个发送文本框
        self.button_send.grid(row=1,column=2,sticky='NSEW')  # 设置串口打开按钮的位置

    '''关闭串口工具窗口触发的函数'''
    def close_window(self):
        ans = messagebox.askyesno('警告',message='确定关闭窗口？')
        print(ans,'ans')
        if ans:
            try:
                self.thd.stop()  # 停止读取串口线程
                '''确保串口会被关掉，修复关掉串口立马更改波特率，显示错误的问题'''
                while self.ser.isOpen():
                    self.ser.close()  # 将串口实例关闭
            except:
                print('关闭窗口')
            self.root.destroy()
        else:
            return

    '''创建串口配置框架'''
    def serial_config_frame(self):
        for temp in enumerate(self.PZMC):
            '''生成标签组'''
            label_name = Label(self.lf, text=temp[1])  # 创建串口标签
            label_name.grid(padx=5,pady=6,column=1,row=temp[0] + 1)   # 设置标签在标签容器中的位置

            '''生成下拉列表框组'''
            if temp[0] == 0:
                self.combobox0 = Combobox(master=self.lf, values=self.CKXX, width=6, height=3,state='readonly')  # 创建下拉列表框
                self.combobox0.current(0)  # 设置下拉列表当前选中项
                self.combobox0.grid(column=2, row=1, sticky='e')  # 设置下拉列表框在标签容器中的位置
                self.combobox0.bind('<Button-1>',self.update_serial_info)
            elif temp[0] == 1:
                self.combobox1 = Combobox(master=self.lf, values=self.BTL, width=6, height=3,state='readonly')  # 创建下拉列表框
                self.combobox1.current(6)   # 设置下拉列表当前选中项
                self.combobox1.grid(column=2, row=2, sticky='e')  # 设置下拉列表框在标签容器中的位置
            elif temp[0] == 2:
                self.combobox2 = Combobox(master=self.lf, values=self.JYW, width=6, height=3,state='readonly')  # 创建下拉列表框
                self.combobox2.current(0)   # 设置下拉列表当前选中项
                self.combobox2.grid(column=2, row=3, sticky='e')  # 设置下拉列表框在标签容器中的位置
            elif temp[0] == 3:
                self.combobox3 = Combobox(master=self.lf, values=self.SJW, width=6, height=3,state='readonly')  # 创建下拉列表框
                self.combobox3.current(3)   # 设置下拉列表当前选中项
                self.combobox3.grid(column=2, row=4, sticky='e')  # 设置下拉列表框在标签容器中的位置
            else:
                self.combobox4 = Combobox(master=self.lf, values=self.TZW, width=6, height=3,state='readonly')  # 创建下拉列表框
                self.combobox4.current(0)   # 设置下拉列表当前选中项
                self.combobox4.grid(column=2, row=5, sticky='e')  # 设置下拉列表框在标签容器中的位置

        self.button_open_serial = Button(self.lf,text='打开串口',command=self.button_open_serial_click)  # 创建串口打开按钮
        self.button_open_serial.grid(row=6,columnspan=5,sticky='s')  # 设置串口打开按钮的位置

    '''串口单击按钮函数'''
    def button_open_serial_click(self):
        if self.button_open_serial['text'] == '打开串口':
            '''下面的try...except...else操作确定当串口被占用报错后，无法在重新打开串口'''
            try:
                self.open_serial_and_config()  # 打开串口
                self.thd = Thread_myself(target=self.serial_read_content)  # 新建线程对象，并且传入串口对象
                self.thd.start()  # 启动串口助手
            except Exception:
                self.button_open_serial['text'] = '打开串口'
                self.result_text.config(state=NORMAL)
                self.result_text.tag_config('text_error_tag', foreground='red')  # 设置插入文本样式
                self.result_text.insert('end','\r\n无法打开串口，请检查串口连接或者是否被占用...\r\n','text_error_tag')
                self.result_text.config(state=DISABLED)
                self.result_text.see(END)  # 文本框总是显示最新内容
            else:
                self.button_open_serial['text'] = '关闭串口'
                self.combobox0.config(state='disabled')  # 打开之后将所有下拉列表框禁用防止误操作
                self.combobox1.config(state='disabled')
                self.combobox2.config(state='disabled')
                self.combobox3.config(state='disabled')
                self.combobox4.config(state='disabled')
        else:
            self.button_open_serial['text'] = '打开串口'
            self.combobox0.config(state='readonly')
            self.combobox1.config(state='readonly')
            self.combobox2.config(state='readonly')
            self.combobox3.config(state='readonly')
            self.combobox4.config(state='readonly')
            try:
                self.thd.stop()  # 停止读取串口线程
                '''确保串口会被关掉，修复关掉串口立马更改波特率，显示错误的问题'''
                while self.ser.isOpen():
                    self.ser.close()  # 将串口实例关闭
            except:
                print('无聊')

    '''打开串口并配置'''
    def open_serial_and_config(self,timeout=5):
        if self.combobox2.get() == 'NONE':  # 判断校验位方式
            parity = 'N'
        elif self.combobox2.get() == 'ODD':
            parity = 'O'
        elif self.combobox2.get() == 'EVEN':
            parity = 'E'
        elif self.combobox2.get() == 'MARK':
            parity = 'M'
        else:
            parity = 'S'

        if self.combobox3.get() == '5':  # 判断数据然后配数据位
            bytesize = 5
        elif self.combobox3.get() == '6':
            bytesize = 6
        elif self.combobox3.get() == '7':
            bytesize = 7
        else:
            bytesize = 8

        if self.combobox4.get() == '1':  # 判断串口停止位
            stopbits = 1
        elif self.combobox4.get() == '1.5':
            stopbits = 1.5
        else:
            stopbits = 2

        '''创建一个串口实例'''
        self.ser = Serial(port=self.combobox0.get(),baudrate=self.combobox1.get(),parity=parity,bytesize=bytesize,stopbits=stopbits,timeout=timeout)
        self.ser.set_buffer_size(rx_size=4096)  # 设置输入缓存去为4096个字节
        self.ser.flushInput()  # 将输入缓存去清空
        print('波特率为%s' %self.ser.baudrate)

    '''读取设备串口信息，并返回串口列表'''
    def read_serial_info(self):
        serial_info = [temp.__getitem__(0) for temp in list_ports.comports()]
        print(serial_info)
        if serial_info:
            return serial_info
        else:
            serial_info = ['No Port!']
            return serial_info

    '''当下拉框被选中时更新串口列表信息'''
    def update_serial_info(self,*args):
        self.combobox0['values'] = self.read_serial_info()

    '''将发送文本框中的内容发送出去'''
    def button_send_serial_click(self):
        '''if逻辑是判断串口有没有打开，如果打开在发送数据，如果没有打开提示打开串口'''
        if self.button_open_serial['text']  == '打开串口':
            messagebox.showwarning('警告','请先打开串口！')
        else:
            try:
                '''判断发送的内容是HEX还是ASCII，根据方式的不同发送方式也不同'''
                if self.serial_sen_hex_bzw:  # HEX方式发送
                    content = self.send_text.get(1.0, 'end').strip()
                    self.ser.write(bytes.fromhex(content))  # HEX方式发送串口数据
                else:  # ASCII方式发送
                    content = self.send_text.get(1.0, 'end').strip().encode().hex()
                    self.ser.write(bytes.fromhex(content))  # ASCII方式发送串口数据
                if content.encode() == b'':
                    messagebox.showwarning('警告', '发送内容不能为空...')
            except Exception:
                messagebox.showerror('错误','请先打开串口...')

    '''串口接收设置'''
    def text_res_config(self):
        '''创建单选框ASCII并配置单选框'''
        self.radiobutton_res_variable = IntVar()  # 设置单选框variable变量，作用是规定value的数值类型
        self.radiobutton_res_dx_acci = Radiobutton(master=self.text_res_con)
        self.radiobutton_res_dx_acci.config(
            text = 'ASCII',  # 单选框名字
            variable = self.radiobutton_res_variable,  # 设置数值类型
            value = 1,  # 设置value数值，同一组单选框中数值必须不一样
            command = self.res_ascii_set  # 绑定单选框单击之后调用的函数
        )
        '''创建单选框HEX并配置单选框'''
        self.radiobutton_res_dx_hex = Radiobutton(master=self.text_res_con)
        self.radiobutton_res_dx_hex.config(
            text = 'HEX',  # 单选框名字
            variable = self.radiobutton_res_variable,  # 设置数值类型
            value = 2,  # 设置value数值，同一组单选框中数值必须不一样
            command = self.res_hex_set   # 绑定单选框单击之后调用的函数
        )
        self.radiobutton_res_variable.set(1)  # 设置那个单选框初始的时候为选中状态
        self.radiobutton_res_dx_acci.grid(padx=5,row=1, column=1, sticky='w')  # 封装ASCII单选框
        self.radiobutton_res_dx_hex.grid(padx=5,row=1,column=2,sticky='e')  # 封装HEX单选框
        self.button_clear_res = Button(master=self.text_res_con,text='清空接收',command=lambda:self.clear_text(self.result_text))  # 添加清空接手区按键
        self.button_clear_res.grid(row=2,sticky='s',columnspan=5,pady=7)  # 将清空按键打包

    '''串口发送设置'''
    def text_sen_config(self):
        '''创建单选框ASCII并配置单选框'''
        self.radiobutton_sen_variable = IntVar()  # 设置单选框variable变量，作用是规定value的数值类型
        self.button_sen_dx_acci = Radiobutton(master=self.text_sen_con)
        self.button_sen_dx_acci.config(
            text = 'ASCII',  # 单选框名字
            variable = self.radiobutton_sen_variable,  # 设置数值类型
            value = 1,  # 设置value数值，同一组单选框中数值必须不一样
            command = self.sen_ascii_set  # 绑定单选框单击之后调用的函数
        )
        '''创建单选框HEX并配置单选框'''
        self.button_sen_dx_hex = Radiobutton(master=self.text_sen_con)
        self.button_sen_dx_hex.config(
            text = 'HEX',  # 单选框名字
            variable = self.radiobutton_sen_variable,  # 设置数值类型
            value = 2,  # 设置value数值，同一组单选框中数值必须不一样
            command = self.sen_hex_set   # 绑定单选框单击之后调用的函数
        )
        self.radiobutton_sen_variable.set(1)  # 设置那个单选框初始的时候为选中状态
        self.button_sen_dx_acci.grid(padx=5,row=1, column=1, sticky='w')  # 封装ASCII单选框
        self.button_sen_dx_hex.grid(padx=5,row=1,column=2,sticky='e')  # 封装HEX单选框
        self.button_sen_clear_res = Button(master=self.text_sen_con,text='清空发送',command=lambda:self.clear_text(self.send_text))  # 添加清空接手区按键
        self.button_sen_clear_res.grid(row=2,sticky='s',columnspan=5,pady=7)  # 将清空按键打包

    '''清空文本空间内容'''
    def clear_text(self,object):
        print('清除')
        object.config(state=NORMAL)  # 设置text对象可以操作
        object.delete(1.0,'end')  # 清空text对象内容
        # object.config(state=DISABLED)  # 设置text对象不可用

    '''设置接收框ASCII转换标志位'''
    def res_ascii_set(self):
        self.serial_res_hex_bzw = False

    '''设置接收框HEX转换标志位'''
    def res_hex_set(self):
        self.serial_res_hex_bzw = True

    '''将发送文本框中的内容以ASCII方式显示'''
    def sen_ascii_set(self):
        self.radiobutton_sen_hex_click_count = 0  # 清零
        self.radiobutton_sen_ascii_click_count += 1  # 单击一次次数+1
        self.serial_sen_hex_bzw = False  # 设置HEX标志位为False
        if not self.serial_sen_hex_bzw and self.radiobutton_sen_ascii_click_count == 1:
            self.send_text.unbind('<Key>')
            self.send_text.unbind('<BackSpace>')
            self.send_text.unbind('<Control--V>')
            self.send_text.unbind('<Control--v>')
            self.send_text.unbind('<Control--C>')
            self.send_text.unbind('<Control--c>')
            self.send_text.config(state=NORMAL)
            send_content = self.send_text.get(1.0,'end').strip()  # 读取输入文本框中的内容
            send_content = ''.join(send_content.split())  # 将16进制的文本去掉空格
            '''实现输入的数据个数不是偶数时，对不成对的数据用0进行补位'''
            if len(send_content) % 2 == 0:
                send_content = [send_content[x * 2:x * 2 + 2] for x in range(len(send_content)//2)]  # 将内容分成2个字符的数组，如：['01','02']
            else:
                temp = send_content
                send_content = [send_content[x * 2:x * 2 + 2] for x in range(len(send_content) // 2)]
                send_content.append(temp[-1].zfill(2))  # 在最后一位前面补0
                send_content = ''.join(send_content)
                send_content = [send_content[x * 2:x * 2 + 2] for x in range(len(send_content) // 2)]  # 将内容分成2个字符的数组，如：['01','02']
                print(send_content, 'send_content')
            send_content = ''.join([chr(int(x,16)) for x in send_content])  # 将上面的数组中的每个元素转换成ASCII格式
            self.clear_text(self.send_text)  # 清空输入文本框内容
            self.send_text.insert('end',send_content.encode())  # 将转换好的内容插入到文本框中

    '''将发送文本框中的内容以HEX方式显示'''
    def sen_hex_set(self):
        self.radiobutton_sen_ascii_click_count = 0  # 清零
        self.radiobutton_sen_hex_click_count += 1  # 单击一次次数+1
        self.serial_sen_hex_bzw = True  # 设置HEX标志位为True
        if self.serial_sen_hex_bzw and self.radiobutton_sen_hex_click_count == 1:
            self.send_text.bind('<Key>',self.key_callback)
            self.send_text.bind('<BackSpace>',self.key_backspace_control_v_callback)
            self.send_text.bind('<Control--V>',self.key_backspace_control_v_callback)
            self.send_text.bind('<Control--v>', self.key_backspace_control_v_callback)
            self.send_text.bind('<Control--C>',self.key_backspace_control_v_callback)
            self.send_text.bind('<Control--c>', self.key_backspace_control_v_callback)
            send_content = self.send_text.get(1.0, 'end').strip()  # 读取输入文本框中的内容
            # send_content = ''.join(send_content.split())  # 将16进制的文本去掉空格
            send_content = send_content.encode().hex()  # 将输入框中的内容转换成16进制

            send_content = ''.join([send_content[x * 2:x * 2 + 2] for x in range(len(send_content) // 2)])  # 转换成16进制的数据进行格式化
            print(send_content, '+++++++++++++++')
            self.clear_text(self.send_text)  # 清空原来的输入框内容
            self.send_text.insert('end', send_content.encode().upper())  # 将转换好的内容插入到文本框中

    '''backspace、control-v、control-c键盘事件回调函数'''
    def key_backspace_control_v_callback(self,event):
        self.send_text.config(state=NORMAL)

    '''发送框绑定键盘事件回调函数'''
    def key_callback(self,event):
        if event.char not in 'abcdefABCDEF0123456789 ':
            self.send_text.config(state=DISABLED)
        else:
            self.send_text.config(state=NORMAL)

    '''类方法：读取串口内容'''
    def serial_read_content(self):
        try:
            '''判断显示方式，self.serial_hex_bzw = True时为16进制显示，self.serial_hex_bzw=False时为ascii显示'''
            if self.serial_res_hex_bzw:
                time_str = time.strftime('[%Y-%m-%d %H:%M:%S]') + '-->HEX\r\n'
                data_res_sum = self.ser.inWaiting()  # 读取输入缓存中有多少个字节数据
                if data_res_sum:
                    text_content = self.ser.read(data_res_sum).hex()  # 将缓存中的数据读取出来
                    text_content = ' '.join([text_content[x*2:x*2+2] for x in range(len(text_content)//2)]).upper()  # 转换成16进制的数据进行格式化,带空格
                    print(text_content,'转换格式之后的文本')
            else:
                time_str = time.strftime('[%Y-%m-%d %H:%M:%S]') + '-->ASCII\r\n'
                data_res_sum = self.ser.inWaiting()  # 读取输入缓存中有多少个字节数据
                if data_res_sum:
                    text_content = self.ser.read(data_res_sum).decode(encoding='utf-8',
                                                                           errors='replace')  # 将缓存中的数据读取出来
                    print('---------------------{}'.format(data_res_sum), text_content)
            time.sleep(0.5)
            if text_content:
                # print('sssssss')
                self.result_text.config(state=NORMAL)  # 打开文本框输入
                self.result_text.tag_config('text_head_tag', foreground='blue')  # 设置插入文本样式
                self.result_text.tag_config('text_tag',foreground='green')  # 设置插入文本样式
                self.result_text.insert('end','\r\n' + time_str + '\r\n','text_head_tag')  # 在文本框中插入数据
                self.result_text.insert('end',text_content + '\r\n','text_tag')  # 在文本框中插入数据
                self.result_text.config(state=DISABLED)  # 禁止文本框输入
                self.result_text.see(END)  # 文本框总是显示最新内容
                text_content = ''
        except Exception:
            print('Fuck you!')

    '''运行软件'''
    def run(self):
        self.serial_config_frame()
        self.text_res_config()
        self.text_sen_config()
        self.root.mainloop()

class Thread_myself(Thread):  # 新建一个Thread子类，重写run方法，让其能够实现暂停
    def __init__(self,target,args=(),kwargs={}):  # 初始化
        super(Thread_myself,self).__init__()  # 调用父类的初始化方法
        self.__running = threading.Event()  # 创建threading.Event类
        self.__running.set()  # 将self.__running设置为true
        self.target = target
        self.args = args
        self.kwargs = kwargs

    '''重写父类thread.Thread的run方法'''
    def run(self):  # 将串口对象传入
        '''读取串口内容并将内容显示到文本框中'''
        while self.__running.isSet():
            self.target(*self.args, **self.kwargs)

    '''停止读取串口数据'''
    def stop(self):
        self.__running.clear()


if __name__ == "__main__":
    main()