import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Combobox
from tkinter import scrolledtext
import subprocess
import threading
import configparser
import time


class OpenDir:
    """选择文件功能"""


    @staticmethod
    def open_file():
        """读取文件名"""


        filepath = filedialog.askopenfilename()
        if filepath:
            
            return filepath

    @staticmethod
    def open_dir():
        """读取目录"""


        dirpath = filedialog.askdirectory()
        if dirpath:
            
            return dirpath


class RgGui:
    """rg-gui主界面"""


    def __init__(self, filepath, dirpath, rg_path):
        """创建主窗口"""


        self.rg_path = rg_path

        self.root = tk.Tk()
        self.root.title('Ripgrep-GUI')
        self.root.geometry("960x540")
        self.root.resizable(width=False, height=False)

        # 选择文件
        self.filepath = filepath
        self.dirpath = dirpath
        self.pathtxt = tk.StringVar(value="未选择文件或目录")

        # 命令执行
        self.cmd_3 = tk.StringVar(value="执行命令")
        self.t1_stop = False
        self.quantity = 0

        self.CheckVar1 = tk.StringVar()
        self.CheckVar2 = tk.StringVar()
        self.CheckVar3 = tk.StringVar()
        self.CheckVar4 = tk.StringVar()
        self.CheckVar5 = tk.StringVar()
        self.CheckVar6 = tk.StringVar()
        self.CheckVar7 = tk.StringVar()

        # 显示
        self.load_dir()
        self.load_cmd()
        self.show_info()
        self.show_options()


    def load_dir(self):
        """目录/文件选择"""


        ld = tk.LabelFrame(self.root, text="文件/目录选择", bg='#5CACEE')
        tk.Button(ld, text="选择目录", height=2, width=19,
                  command=self.open_dir).pack(pady=10)
        tk.Button(ld, text="选择文件", height=2, width=19,
                  command=self.open_file).pack()

        ld.place(width=190, height=150)


    def open_file(self):
        """打开文件"""


        path = self.filepath()
        if path:
            self.pathtxt.set(f"{path}")


    def open_dir(self):
        """打开目录"""


        path = self.dirpath()
        if path:
            self.pathtxt.set(f"{path}")


    def load_cmd(self):
        """搜索功能"""


        lc = tk.LabelFrame(self.root, text="搜索功能", bg='#5CACEE')
        tk.Label(lc, text="条件1",).place(x=3, y=15)
        self.cmd_1 = tk.Entry(lc, width=50,)
        self.cmd_1.place(x=45, y=10, height=35)
        tk.Label(lc, text="条件2",).place(x=3, y=80)
        self.cmd_2 = tk.Entry(lc, width=50,)
        self.cmd_2.place(x=45, y=75, height=35)

        self.search_but = tk.Button(lc, text="搜索", height=2, width=23,
                                    command=self.run_cmd)
        self.search_but.place(x=420)
        tk.Button(lc, text="停止", height=1, width=10,
                  command=self.stop_command).place(x=420, y=50)
        tk.Button(lc, text="清空", height=1, width=10,
                  command=self.clear_output).place(x=510, y=50)
        tk.Label(lc, text="编码",).place(x=420, y=90)
        bm = ['', '-E UTF-8', '-E GBK']
        self.bmm = Combobox(lc, values=bm, width=16)
        self.bmm.place(x=455, y=90)

        lc.place(x=190, width=602, height=150,)


    def run_cmd(self):
        """执行搜索命令"""


        c1 = self.cmd_1.get()
        c2 = self.cmd_2.get()
        self.search_but.config(state='disabled')

        if c1 and c2 and self.pathtxt.get() != "未选择文件或目录":
            c3 = f'{self.rg_path} {c1} {self.bmm.get()} {self.CheckVar2.get()} {self.CheckVar3.get()} {self.CheckVar4.get()} {self.CheckVar6.get()} {self.pathtxt.get()} | {self.rg_path} {c2} {self.CheckVar1.get()} {self.CheckVar2.get()} {self.CheckVar4.get()} {self.CheckVar5.get()} {self.CheckVar7.get()} {self.bmm.get()}'
            self.cmd_3.set(c3)

            self.t1 = threading.Thread(
                target=self.run_command_in_background, args=(c3,))
            self.t1.start()

        elif c1 and self.pathtxt.get() != "未选择文件或目录":
            c3 = f'{self.rg_path} {c1} {self.bmm.get()} {self.CheckVar1.get()} {self.CheckVar2.get()} {self.CheckVar3.get()} {self.CheckVar4.get()} {self.CheckVar5.get()} {self.CheckVar6.get()} {self.CheckVar7.get()} {self.pathtxt.get()}'
            self.cmd_3.set(c3)

            self.t1 = threading.Thread(
                target=self.run_command_in_background, args=(c3,))
            self.t1.start()

        else:
            messagebox.askokcancel(title='错误', message="命令错误或未选择目录/文件")
            self.search_but.config(state='normal')


    def run_command_in_background(self, c3):
        """实时输出线程"""
        

        self.t1_stop = True

        try:
            # 使用 subprocess 执行命令，并获取实时输出
            self.process = subprocess.Popen(
                c3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True, encoding='utf-8', )
            

            for stdout_line in iter(self.process.stdout.readline, ""):
                if stdout_line:  # 确保读取到有效数据
                    self.output_text.insert(tk.END, stdout_line)
                    self.output_text.yview(tk.END)
                    self.quantity += 1
                    time.sleep(0.001)

            # 等待完成
            self.process.stdout.close()
            self.process.stderr.close()
            self.process.wait()

            # 输出数据
            self.output_text.insert(
                tk.END, '###############搜索完成###############\n')
            self.output_text.insert(
                tk.END, f'共计 {self.quantity} 条数据\n')
            self.output_text.yview(tk.END)

        except UnicodeDecodeError:
            self.output_text.insert(
                tk.END, "!!!!!!!!!!!!!编码错误!!!!!!!!!!!!!\n")
            self.output_text.yview(tk.END)
            self.stop_command()

        except ValueError:
            # print('io错误')
            self.output_text.insert(
                tk.END, "###############命令已停止###############\n")
            self.output_text.insert(
                tk.END, f'共计 {self.quantity} 条数据\n')
            self.output_text.yview(tk.END)

        except Exception as e:
            self.output_text.insert(
                tk.END, "###############命令已停止###############\n")
            self.output_text.insert(tk.END, f"错误1:{e}\n")
            self.output_text.yview(tk.END)

        finally:
            # 重置参数
            self.t1_stop = False
            self.search_but.config(state='normal')
            self.quantity = 0

    def clear_output(self):
        """清空输出内容"""


        self.output_text.delete(1.0, tk.END)
        self.cmd_3.set('执行命令')


    def stop_command(self):
        """停止命令"""


        try:
            if self.t1_stop:
                # 截取exe
                rg_exe = str(self.rg_path).split('\\')
                kill_rg = subprocess.Popen(
                    f'taskkill /F /IM {rg_exe[-1]}', shell=True, encoding='utf-8',)
                kill_rg.wait()
                self.process.stdout.close()
                self.process.stderr.close()

                # 中途停止逻辑
                if self.quantity < 3:
                    self.output_text.insert(
                        tk.END, "###############命令已停止###############\n")
                    self.output_text.yview(tk.END)

        except Exception as e:
            self.output_text.insert(tk.END, f"停止命令失败: {str(e)}\n")

        finally:
            # 重置搜索按钮
            self.search_but.config(state='normal')


    def show_info(self):
        """显示搜索内容"""


        si = tk.LabelFrame(self.root, text="查询输出", bg='#5CACEE')
        tk.Label(si, textvariable=self.pathtxt, font=(
            "黑体", 8)).pack(pady=1, anchor='nw')
        tk.Label(si, textvariable=self.cmd_3, font=("黑体", 8)).pack(anchor='nw')
        self.output_text = scrolledtext.ScrolledText(
            si, bg='black', fg='lime', insertbackground='white')
        self.output_text.pack(fill="x", ipadx=10, ipady=10)
        si.place(y=150, width=792, height=389)



    def show_options(self):
        """参数内容显示"""

        op = tk.LabelFrame(self.root, text="可选参数", bg='#5CACEE')

        n = tk.Checkbutton(op, text="-n:显示行号", bg='#5CACEE',
                           variable=self.CheckVar1, onvalue='-n', offvalue='')
        n.grid(row=1, column=0, padx=1, pady=1,)
        S = tk.Checkbutton(op, text="-S:智能大小写", bg='#5CACEE',
                           variable=self.CheckVar2, onvalue='-S', offvalue='')
        S.grid(row=2, column=0, padx=1, pady=1)
        U = tk.Checkbutton(op, text="-U:跨多行搜索", bg='#5CACEE',
                           variable=self.CheckVar3, onvalue='-U', offvalue='')
        U.grid(row=3, column=0, padx=1, pady=1)
        i = tk.Checkbutton(op, text="-i:不区分大小写", bg='#5CACEE',
                           variable=self.CheckVar4, onvalue='-i', offvalue='')
        i.grid(row=4, column=0, padx=1, pady=1)

        I = tk.Checkbutton(op, text="-I:不显示文件路径", bg='#5CACEE',
                           variable=self.CheckVar7, onvalue='-I', offvalue='')
        I.grid(row=5, column=0, padx=1, pady=1)        

        stats = tk.Checkbutton(op, text="--stats:搜索统计信息", bg='#5CACEE',
                               variable=self.CheckVar5, onvalue='--stats', offvalue='')
        stats.grid(row=6, column=0, padx=1, pady=1)
        a = tk.Checkbutton(op, text="-a:二进制文件转文本搜索", bg='#5CACEE',
                           variable=self.CheckVar6, onvalue='-I', offvalue='')
        a.grid(row=7, column=0, padx=1, pady=1)
       


        op.place(x=792, height=539, width=167)


    def run_show(self):
        """启动"""

        self.root.mainloop()


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")
    rg_path = config['rgpath']['path']
    app = RgGui(OpenDir.open_file, OpenDir.open_dir, rg_path)
    app.run_show()
