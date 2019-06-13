import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import requests
# 服务器信息
# url = ['http://192.168.0.145:9998', 'http://api.singmap.com']
# # none_url = 'http://api.singmap.com'
# img_url = ''

# # 接口路径
# login = '/broke-manager-service/sysuser/login'
# queryProject = '/broke-manager-service/project/queryProject'
# querySitePlan = '/broke-manager-service/siteplan/querySitePlan'
# updateSiteContent = '/broke-manager-service/siteplan/updateSiteContent'

# #用户信息
# user_name = ''
# user_token = ''
# user_email = ''
# user_password = ''
# user_Id = ''
# brokeId = ''
# projectId = ''
# sitePlanId = ''
# '''松耦合'''

pd = R'E:\新联国际\地产项目\自动画图\HUATU\config.ini'
RD = configparser.ConfigParser()
RD.read(pd, encoding='utf-8')
fp = open(pd, 'w',encoding='utf-8')
# print(RD.get('DATABASE', 'database'))
RD.set('USER', 'user_name', 'CCC')
RD.write(fp)
fp.close()

def down_png(pwd):
    with open('.\\img01.jpg', 'ab') as f:
        r = requests.get()
        f.write(r.content)
        f.close()




# 登录
class MyDialog(tk.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.title('登录')
        # self.geometry('450x450')
        # self.none_url = none_url
        self.parent = parent # 显式地保留父窗口
        self.setup_UI()

    def setup_UI(self):
        # def go(*args):  #处理事件，*args表示可变参数
        #     self.none_url = comboxlist.get()

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
            row3, text="登录", width=20,
            command=self.logins).pack(side=tk.BOTTOM)

        # 登录提示
        row5 = tk.Frame(self)
        self.var1 = tk.StringVar()
        row5.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(
            row5, fg='red', textvariable=self.var1,
            width=20).pack(side=tk.LEFT)

    def logins(self):

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
class PopupDialog(tk.Toplevel):
  def __init__(self, parent):
    super().__init__()
    self.title('设置用户信息')
    self.parent = parent # 显式地保留父窗口
    def show_msg(*args):
        return players.get()
    
    def alls():
        players["values"] = ("1", "2", "3","1", "2", "3")
        players.set("演员表")
    row2 = tk.Frame(self)
    row2.pack(fill="x")
    self.name = tk.StringVar()
    players = ttk.Combobox(row2, textvariable=self.name)
    players["values"] = ("成龙", "刘德华", "周星驰")
    players["state"] = "readonly"
    
    players.current(1)
    # players.set("演员表")
    # print(players.get())
    
    players.bind("<<ComboboxSelected>>", show_msg)

    tk.Button(row2, text="登录", width=20,command=self.show_msg).pack(side=tk.LEFT)
    players.pack(side=tk.LEFT)

    # 第一行（两列）
    # row1 = tk.Frame(self)
    # row1.pack(fill="x")
    # tk.Label(row1, text='姓名：', width=8).pack(side=tk.LEFT)
    # self.name = tk.StringVar()
    # tk.Entry(row1, textvariable=self.name, width=20).pack(side=tk.LEFT)

    # # 第二行
    # row2 = tk.Frame(self)
    # row2.pack(fill="x", ipadx=1, ipady=1)
    # tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
    # self.age = tk.IntVar()
    # tk.Entry(row2, textvariable=self.age, width=20).pack(side=tk.LEFT)
    # # 第三行
    # row3 = tk.Frame(self)
    # row3.pack(fill="x")
    # tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
    # tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)
  def ok(self):
    # 显式地更改父窗口参数
    self.parent.name = self.name.get()
    self.parent.age = self.show_msg()
    print(self.parent.age)
    # 显式地更新父窗口界面
    self.parent.l1.config(text=self.parent.name)
    self.parent.l2.config(text=self.parent.age)
    self.destroy() # 销毁窗口
  def cancel(self):
    self.destroy()





# 主窗
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #self.pack() # 若继承 tk.Frame ，此句必须有！
        self.title('自动画图工具')
        self.geometry('1362x794')
        self.age = 30
        self.setupUI()
        

    def setupUI(self):
        def set_pro(datas):
            self.players["values"] = (datas)

        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(
            row3, text="登录", width=20,
            command=self.setup_config).pack(side=tk.LEFT)
        tk.Label(row3, text='用户：', width=8).pack(side=tk.LEFT)
        self.user_names = tk.IntVar(value=RD.get('USER', 'username'))
        tk.Label(
            row3, textvariable=self.user_names, width=10).pack(side=tk.LEFT)
        

        #选择项目
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Button(
            row1, text="选择项目", width=20,
            command=self.setup_config).pack(side=tk.LEFT)
        tk.Label(row1, text='：', width=8).pack(side=tk.LEFT)
        self.project_name = tk.IntVar(value=RD.get('USER', 'username'))
        tk.Label(
            row1, textvariable=self.project_name, width=10).pack(side=tk.LEFT)
        self.l2 = tk.Label(row1, text=self.age, width=20)
        self.l2.pack(side=tk.LEFT)

        #选择building 
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Button(
            row2, text="选择building", width=20,
            command=self.get_pro).pack(side=tk.LEFT)
        tk.Label(row2, text='：', width=8).pack(side=tk.LEFT)
        self.buildings = tk.IntVar(value=RD.get('USER', 'username'))
        tk.Label(
            row2, textvariable=self.buildings, width=10).pack(side=tk.LEFT)

        # tk.Label(row2, text='选择楼栋：', width=8).pack(side=tk.LEFT)
        # self.project_list1 = tk.StringVar()
        # self.players = ttk.Combobox(row2, textvariable=self.project_list1)
        # self.players["values"] = ['暂无楼栋']
        # # players["state"] = "readonly"
        # self.players.current(0)
        # self.players.pack(side=tk.LEFT)

    def setup_config(self):
        # 接收弹窗的数据
        res = self.ask_userinfo()
        # print(res)
        # if res is None: return
        self.user_names.set(RD.get('USER', 'username'))
        # print(res.user_all.get('code'))

        if res.user_all.get('code') == '0' :
            print(RD.get('USER', 'userid'))
            data= {
                'userId': RD.get('USER', 'userid'),
                'token': RD.get('USER', 'token'),
                'brokeId': RD.get('USER', 'brokeid'),
                'pageSize': 50,
                'pageNo': 1,
                'projectName': ''
            }
            self.project = requests.get(RD.get('HTTP','none_url')+RD.get('HTTP','queryproject'),params = data).json()
            if self.project['code'] == '0' :
                for i in self.project['datas']['lists']:
                    print(i['projectName'])
                    self.set_pro(('1','2','3'))
                    print(i['projectName'])
            self.project_list = self.project
            # print(self.project)

    # 弹窗
    def ask_userinfo(self):
        inputDialog = MyDialog(self)
        self.wait_window(inputDialog)  # 这一句很重要！！！
        return inputDialog
    
    #
    def get_pro(self):
        pw = PopupDialog(self)
        self.wait_window(pw) # 这一句很重要！！！
        return
if __name__ == '__main__':
    app = MyApp()
    app.mainloop()