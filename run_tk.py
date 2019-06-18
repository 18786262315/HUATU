import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Scrollbar
import configparser
import requests
from PIL import Image,ImageTk
import os

pd = R'E:\新联国际\地产项目\自动画图\HUATU\config.ini'
RD = configparser.ConfigParser()
RD.read(pd, encoding='utf-8')



# 登录
class MyDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('登录')
        self.parent = parent  # 显式地保留父窗口
        self.setup_UI()

    def setup_UI(self):


        # 工作环境输入框
        row4 = tk.Frame(self)
        row4.pack(fill="x")
        tk.Label(row4, text='账户：', width=8).pack(side=tk.LEFT)
        self.environment = tk.StringVar(value=RD.get('HTTP', 'url1'))
        tk.Entry(
            row4, textvariable=self.environment, width=20).pack(side=tk.LEFT)

        # 用户名输入框
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Label(row1, text='账户：', width=8).pack(side=tk.LEFT)
        self.name = tk.StringVar(value='ccc@mixgo.com')
        tk.Entry(row1, textvariable=self.name, width=20).pack(side=tk.LEFT)

        # 密码输入框
        row2 = tk.Frame(self)
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='密码：', width=8).pack(side=tk.LEFT)
        self.password = tk.IntVar(value='123456')
        tk.Entry(
            row2, textvariable=self.password, show="*",
            width=20).pack(side=tk.LEFT)

        # 登录按钮
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(
            row3, text="登录", width=20,bd=5,
            command=self.logins).pack(side=tk.BOTTOM)

        # 登录提示
        row5 = tk.Frame(self)
        self.var1 = tk.StringVar()
        row5.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(
            row5, fg='red', textvariable=self.var1,
            width=20).pack(side=tk.LEFT)

    def logins(self):
        # 登录
        data = {
            'userId': '',
            'token': '',
            'brokeId': '',
            'email': self.name.get(),
            'password': self.password.get()
        }
        print(RD.get('HTTP', 'url1'))
        self.user_all = requests.post(
            self.environment.get() + RD.get('HTTP', 'login'),
            data=data).json()

        if self.user_all.get('code') == '0':
            print(self.user_all['datas'])
            RD['USER'] = self.user_all['datas']
            RD['HTTP']['img_url'] = self.user_all['url']
            RD['HTTP']['none_url'] = self.environment.get()
            with open(pd, 'w', encoding='utf-8') as file:
                RD.write(file)  # 数据写入配置文件

            messagebox.showinfo('登录成功', self.user_all['msg'])
            self.destroy()  # 销毁窗口
        else:
            self.var1.set('账户或密码错误！！')


#获取项目
class Project(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('项目搜索')
        self.parent = parent  # 显式地保留父窗口

        # 搜索
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        self.projectname = tk.StringVar(value='请输入项目名称。。') #输入框
        tk.Entry(row1, textvariable=self.projectname, bd=5).pack(side=tk.LEFT)
        tk.Button(row1, text="搜索", width=7,bd=5, command=self.search).pack(side=tk.LEFT) #搜索按钮

        # 选择框
        row2 = tk.Frame(self)
        row2.pack(fill="x") 
        scrollbar = Scrollbar(row2)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.lb3 = Listbox(row2,selectmode=tk.BROWSE,height=10,width=30,bd=5,yscrollcommand=scrollbar.set) # 选择框
        self.lb3.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.lb3.yview) # scrollbar 选择框滚动条
        scrollbar.pack(side=tk.RIGHT, fill='y') 

        # 错误提示以及确认按钮
        row3 = tk.Frame(self)
        row3.pack(fill="y") 
        self.msg = tk.IntVar(value='')
        tk.Label(
            row3, textvariable=self.msg, width=10,fg='red').pack(side=tk.LEFT)

        tk.Button(
            row3, text="确认", width=7, command=self.ok, bd=5).pack(
                side=tk.RIGHT, fill='x') # 

    def search(self):
        data = {
            'userId': RD.get('USER', 'userid'),
            'token': RD.get('USER', 'token'),
            'brokeId': RD.get('USER', 'brokeid'),
            'pageSize': '100',
            'pageNo': '1',
            'projectName': self.projectname.get()
        }
        project = requests.get(RD.get('HTTP', 'none_url') + RD.get('HTTP', 'queryproject'),
            params=data).json() #项目搜索接口
        self.project_lists = project['datas']['lists'] #项目列表
        print(self.project_lists)
        if len(self.project_lists) ==0:
            self.msg.set('项目不存在!')
        else:
            self.lb3.delete([0],'end') #清空列表
            for b,i in enumerate(self.project_lists):
                # 修改列表展示数据
                self.lb3.insert('end', str(i['projectName'])) 
    def ok(self):
        none_pro = self.project_lists[int(self.lb3.curselection()[0])]
        RD['PROJECT']['projectId'] = none_pro['projectId']
        RD['PROJECT']['projectName'] = none_pro['projectName']
        with open(pd, 'w', encoding='utf-8') as file:
            RD.write(file)  # 数据写入配置文件
        self.destroy()  # 销毁窗口





# 获取buildding
class BuildDing(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('buildding列表')
        self.parent = parent  # 显式地保留父窗口
        self.setupUI()
    def setupUI(self):
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Button(row1, text="获取列表", width=10,bd=5, command=self.search).pack(side=tk.LEFT) #搜索按钮

        # 选择框
        row2 = tk.Frame(self)
        row2.pack(fill="x") 
        scrollbar = Scrollbar(row2)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.lb3 = Listbox(row2,selectmode=tk.BROWSE,height=10,width=30,yscrollcommand=scrollbar.set) # 选择框
        self.lb3.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.lb3.yview) # scrollbar 选择框滚动条
        scrollbar.pack(side=tk.RIGHT, fill='y') 

        # 错误提示以及确认按钮
        row3 = tk.Frame(self)
        row3.pack(fill="y") 
        self.msg = tk.IntVar(value='')
        tk.Label(
            row3, textvariable=self.msg, width=10,fg='red').pack(side=tk.LEFT)

        tk.Button(
            row3, text="确认", width=7, command=self.ok, bd=5).pack(
                side=tk.RIGHT, fill='y') 
        # tk.Button(
        #     row3, text="查看图片", width=7, command=self.ok, bd=5).pack(
        #         side=tk.RIGHT, fill='y') 

    def search(self):
        # 获取列表并展示
        data = {
        'userId': RD.get('USER', 'userid'),
        'token': RD.get('USER', 'token'),
        'brokeId': RD.get('USER', 'brokeid'),
        'projectId': RD.get('PROJECT', 'projectid'),
        }
        project = requests.get(RD.get('HTTP', 'none_url') + RD.get('HTTP', 'querysiteplan'),
            params=data).json() #项目搜索接口
        self.project_lists = project['datas']['lists'] #项目列表
        if len(self.project_lists) ==0:
            self.msg.set('列表为空!')
        else:
            self.lb3.delete([0],'end') #清空列表
            for b,i in enumerate(self.project_lists):
                # 修改列表展示数据
                self.lb3.insert('end', str(i['sitePlanName'])) 
    def ok(self):
        # 确认
        none_pro = self.project_lists[int(self.lb3.curselection()[0])]
        if none_pro['img'] != None:
            RD['SITEPLAN']['buildingId'] = none_pro['buildingId']
            RD['SITEPLAN']['sitePlanName'] = none_pro['sitePlanName']
            RD['SITEPLAN']['img'] = none_pro['img']
            (file_pwd,file_name)=os.path.split(none_pro['img'])
            with open(R'.\\IMGS\\'+file_name, 'ab') as f:
                r = requests.get(RD.get('HTTP', 'img_url')+none_pro['img'])
                f.write(r.content)
                f.close()
            
            RD['HTTP']['img_pwd'] = R'.\\IMGS\\'+file_name        
            with open(pd, 'w', encoding='utf-8') as file:
                RD.write(file)  # 数据写入配置文件
            self.destroy()  # 销毁窗口
        else:
            self.msg.set('没有图片!')


        


class Photo(tk.Toplevel):
    # 图片查看
    def __init__(self, parent):
        super().__init__()
        self.title('查看图片')
        # self.geometry('1362x794')
        self.parent = parent  # 显式地保留父窗口
        self.setupUI()
    def setupUI(self):
        row1 = tk.Frame(self)
        row1.pack(fill = 'x')
        img_pwd = RD.get('HTTP', 'img_pwd')
        self.img = Image.open(img_pwd)
        (h,w)=self.img.size
        if h > 1920 or w > 1080 :
            self.img = self.img.resize((int(h/2), int(w/2)), Image.ANTIALIAS) #图片尺寸调整
        self.photo = ImageTk.PhotoImage(self.img)#在root实例化创建，否则会报错
        label = tk.Label(row1,image=self.photo)
        label.pack()


class Run_Go(tk.Toplevel):
    # 图片查看
    def __init__(self, parent):
        super().__init__()
        self.title('查看图片')
        # self.geometry('1362x794')
        self.parent = parent  # 显式地保留父窗口
        self.setupUI()
    def setupUI(self):
        row1 = tk.Frame(self)
        row1.pack(fill = 'x')
        img_pwd = RD.get('HTTP', 'img_pwd')
        self.img = Image.open(img_pwd)
        (h,w)=self.img.size
        if h > 1920 or w > 1080 :
            self.img = self.img.resize((int(h/2), int(w/2)), Image.ANTIALIAS) #图片尺寸调整
        self.photo = ImageTk.PhotoImage(self.img)#在root实例化创建，否则会报错
        label = tk.Label(row1,image=self.photo)
        label.pack()





# 主窗
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.pack() # 若继承 tk.Frame ，此句必须有！
        self.title('自动画图工具')
        self.geometry('450x450')
        # self.age = 10
        # self.setup_config()
        self.setupUI()

    def setupUI(self):
        def set_pro(datas):
            self.players["values"] = (datas)

        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Button(
            row1, text="登录", width=20,height=3,bd=5,
            command=self.setup_config).pack(side=tk.LEFT)
        # tk.Label(row1, text='用户：', width=8).pack(side=tk.LEFT)
        self.user_names = tk.IntVar(value=RD.get('USER', 'username'))
        tk.Label(
            row1, textvariable=self.user_names, width=10).pack(side=tk.LEFT)

        #选择项目
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Button(
            row2, text="选择项目", width=20,height=3,bd=5,
            command=self.get_project).pack(side=tk.LEFT)

        self.project_name = tk.IntVar(value=RD.get('PROJECT', 'projectname'))
        tk.Label(
            row2, textvariable=self.project_name, width=10).pack(side=tk.LEFT)
        # self.l2 = tk.Label(row1, text=self.age, width=20)
        # self.l2.pack(side=tk.LEFT)

        #选择building
        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(
            row3, text="选择building", width=20,height=3,bd=5,
            command=self.get_siteplan).pack(side=tk.LEFT)
        # 图片查看
        tk.Button(
            row3, text="查看图片", width=6,height=1,bd=5,
            command=self.img_look).pack(side=tk.LEFT)
        # 执行画图工具
        row4 = tk.Frame(self)
        row4.pack(fill="x")
        tk.Button(
            row4, text="开始执行", width=20,height=3,bd=5,
            command=self.get_siteplan).pack(side=tk.LEFT)

        row5 = tk.Frame(self)
        row5.pack(fill="x")
        tk.Button(
            row5, text="复制", width=20,height=3,bd=5,
            command=self.get_siteplan).pack(side=tk.LEFT)
        self.project_name = tk.IntVar(value=RD.get('USER', 'username'))
        tk.Label(
            row5, textvariable=self.project_name, width=10).pack(side=tk.LEFT)

    def setup_config(self):
        # 接收弹窗的数据
        res = self.ask_userinfo()
        # print(res)
        # if res is None: return
        self.user_names.set(RD.get('USER', 'username'))

    # 登录弹窗
    def ask_userinfo(self):
        inputDialog = MyDialog(self)
        self.wait_window(inputDialog)  # 这一句很重要！！！
        return inputDialog

    #处理项目列表
    def get_project(self):
        res = self.get_pro()
        self.project_name.set(RD.get('PROJECT', 'projectname'))

    #获取项目弹窗
    def get_pro(self):
        pw = Project(self)
        self.wait_window(pw)  # 这一句很重要！！！
        return pw

    # 获取siteplan列表
    def get_siteplan(self):
        res = self.get_siteplans()
        self.user_names.set(RD.get('USER', 'username'))

    # siteplan选择弹窗
    def get_siteplans(self):
        pws = BuildDing(self)
        self.wait_window(pws)  # 这一句很重要！！！
        return pws

    def img_look(self):
        imgs = Photo(self)
        self.wait_window(imgs)

    # 获取siteplan列表
    def run_ts(self):
        res = self.run_buildings()
    # siteplan选择弹窗
    def run_buildings(self):
        run_go = Run_Go(self)
        self.wait_window(run_go)  # 这一句很重要！！！
        return run_go


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()