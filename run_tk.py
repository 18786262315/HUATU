import tkinter as tk
from tkinter import ttk, messagebox, Listbox, Scrollbar
from PIL import Image, ImageTk
import cv2
import numpy as np
import re,copy,requests,json,os,configparser

pd = '.\\config.ini'
RD = configparser.ConfigParser()
RD.read(pd, encoding='utf-8')


#################################################################


# 登录
class MyDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('登录')
        
        self.parent = parent  # 显式地保留父窗口

        self.setup_UI()
    def setup_UI(self):
        self.img = Image.open(r'.\IMGS\003.png')
        self.photo = ImageTk.PhotoImage(self.img)  #在root实例化创建，否则会报错
        label = tk.Label(self,image=self.photo,bg='#AFEEEE')
        label.pack()
        # self.attributes("-toolwindow", 1)
        # self.wm_attributes("-topmost", 1)
        # 工作环境输入框
        
        row4 = tk.Frame(self,bg='#AFEEEE')
        row4.pack(fill="x")
        tk.Label(row4, text='环境', width=8,bg='#AFEEEE').pack(side=tk.LEFT)
        self.environment = tk.StringVar(value=RD.get('HTTP', 'url2'))
        tk.Entry(
            row4, textvariable=self.environment, width=20).pack(side=tk.BOTTOM)

        # 用户名输入框
        row1 = tk.Frame(self,bg='#AFEEEE')
        row1.pack(fill="x")
        tk.Label(row1, text='账户', width=8,bg='#AFEEEE').pack(side=tk.LEFT)
        self.name = tk.StringVar(value=RD.get('USER', 'email'))
        tk.Entry(row1, textvariable=self.name, width=20).pack(side=tk.BOTTOM)

        # 密码输入框
        row2 = tk.Frame(self,bg='#AFEEEE')
        row2.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row2, text='密码', width=8,bg='#AFEEEE').pack(side=tk.LEFT)
        self.passwd = tk.StringVar(value=RD.get('USER', 'password'))
        tk.Entry(row2, textvariable=self.passwd,width=20,show='*').pack(side=tk.BOTTOM)

        # 登录按钮
        row3 = tk.Frame(self,bg='#AFEEEE')
        row3.pack(fill="x")
        tk.Button(
            row3, text="登录", width=20, bd=5,
            command=self.logins).pack(side=tk.BOTTOM)

        # 登录提示
        row5 = tk.Frame(self,bg='#AFEEEE')
        self.var1 = tk.StringVar()
        row5.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(
            row5, fg='red', textvariable=self.var1,
            width=20,bg='#AFEEEE').pack(side=tk.BOTTOM)
    def logins(self):
        # 登录
        data = {
            'userId': '',
            'token': '',
            'brokeId': '',
            'email': self.name.get(),
            'password': self.passwd.get()
        }
        # print(RD.get('HTTP', 'url1'))
        self.user_all = requests.post(
            self.environment.get() + RD.get('HTTP', 'login'),
            data=data).json()

        if self.user_all.get('code') == '0':
            # print(self.user_all['datas'])
            RD['USER'] = self.user_all['datas']
            RD['HTTP']['img_url'] = self.user_all['url']
            RD['HTTP']['none_url'] = self.environment.get()
            RD['USER']['password'] = self.passwd.get()
            with open(pd, 'w', encoding='utf-8') as file:
                RD.write(file)  # 数据写入配置文件

            self.destroy()  # 销毁窗口
        else:
            self.var1.set('账户或密码错误！！')

##########################################################################

#获取项目
class Project(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('项目搜索')
        self.parent = parent  # 显式地保留父窗口
        self.setup_UI()

    def setup_UI(self):
        # self.attributes("-toolwindow", 1)
        # self.wm_attributes("-topmost", 1)
        # 搜索
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        self.projectname = tk.StringVar(value='请输入项目名称。。')  #输入框
        tk.Entry(row1, textvariable=self.projectname, bd=5).pack(side=tk.LEFT)
        tk.Button(
            row1, text="搜索", width=7, bd=5, command=self.search).pack(
                side=tk.LEFT)  #搜索按钮

        # 选择框
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        scrollbar = Scrollbar(row2)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.lb3 = Listbox(row2,selectmode=tk.BROWSE,height=10,width=30,bd=5,yscrollcommand=scrollbar.set)  # 选择框
        self.lb3.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.lb3.yview)  # scrollbar 选择框滚动条
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # 错误提示以及确认按钮
        row3 = tk.Frame(self)
        row3.pack(fill="y")
        self.msg = tk.IntVar(value='')
        tk.Label(
            row3, textvariable=self.msg, width=10, fg='red').pack(side=tk.LEFT)

        tk.Button(
            row3, text="确认", width=7, command=self.ok, bd=5).pack(
                side=tk.RIGHT, fill='x')  #

    def search(self):
        data = {
            'userId': RD.get('USER', 'userid'),
            'token': RD.get('USER', 'token'),
            'brokeId': RD.get('USER', 'brokeid'),
            'pageSize': '100',
            'pageNo': '1',
            'projectName': self.projectname.get()
        }
        project = requests.get(
            RD.get('HTTP', 'none_url') + RD.get('HTTP', 'queryproject'),
            params=data).json()  #项目搜索接口
        self.project_lists = project['datas']['lists']  #项目列表
        # print(self.project_lists)
        if len(self.project_lists) == 0:
            self.msg.set('项目不存在!')
        else:
            self.lb3.delete([0], 'end')  #清空列表
            for b, i in enumerate(self.project_lists):
                # 修改列表展示数据
                self.lb3.insert('end', str(i['projectName']))

    def ok(self):
        none_pro = self.project_lists[int(self.lb3.curselection()[0])]
        RD['PROJECT']['projectId'] = none_pro['projectId']
        RD['PROJECT']['projectName'] = none_pro['projectName']
        with open(pd, 'w', encoding='utf-8') as file:
            RD.write(file)  # 数据写入配置文件
        self.destroy()  # 销毁窗口

##########################################################################

# 获取buildding
class BuildDing(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('buildding列表')
        self.parent = parent  # 显式地保留父窗口
        self.setupUI()

    def setupUI(self):
        # self.attributes("-toolwindow", 1)
        # self.wm_attributes("-topmost", 1)
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        tk.Button(
            row1, text="获取列表", width=10, bd=5, command=self.search).pack(
                side=tk.LEFT)  #搜索按钮

        # 选择框
        row2 = tk.Frame(self)
        row2.pack(fill="x")
        scrollbar = Scrollbar(row2)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.lb3 = Listbox(row2,selectmode=tk.BROWSE,height=10,width=30,yscrollcommand=scrollbar.set)  # 选择框
        self.lb3.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.lb3.yview)  # scrollbar 选择框滚动条
        scrollbar.pack(side=tk.RIGHT, fill='y')

        # 错误提示以及确认按钮
        row3 = tk.Frame(self)
        row3.pack(fill="y")
        self.msg = tk.IntVar(value='')
        tk.Label(
            row3, textvariable=self.msg, width=10, fg='red').pack(side=tk.LEFT)

        tk.Button(
            row3, text="确认", width=7, command=self.ok, bd=5).pack(
                side=tk.RIGHT, fill='y')

    def search(self):
        # 获取列表并展示
        data = {
            'userId': RD.get('USER', 'userid'),
            'token': RD.get('USER', 'token'),
            'brokeId': RD.get('USER', 'brokeid'),
            'projectId': RD.get('PROJECT', 'projectid'),
        }
        project = requests.get(
            RD.get('HTTP', 'none_url') + RD.get('HTTP', 'querysiteplan'),
            params=data).json()  #项目搜索接口
        self.project_lists = project['datas']['lists']  #项目列表
        if len(self.project_lists) == 0:
            self.msg.set('列表为空!')
        else:
            self.lb3.delete([0], 'end')  #清空列表
            for b, i in enumerate(self.project_lists):
                # 修改列表展示数据
                self.lb3.insert('end', str(i['sitePlanName']))

    def ok(self):
        # 确认
        none_pro = self.project_lists[int(self.lb3.curselection()[0])]
        if none_pro['img'] != None:
            RD['SITEPLAN']['sitePlanId'] = none_pro['sitePlanId']
            RD['SITEPLAN']['sitePlanName'] = none_pro['sitePlanName']
            RD['SITEPLAN']['img'] = none_pro['img']
            (file_pwd, file_name) = os.path.split(none_pro['img'])
            if os.path.isfile('.\\IMGS\\' + file_name):
                pass
            else:
                with open('.\\IMGS\\' + file_name, 'ab') as f:
                    r = requests.get(RD.get('HTTP', 'img_url') + none_pro['img'])
                    f.write(r.content)
                    f.close()

            RD['HTTP']['img_pwd'] = '.\\IMGS\\' + file_name
            with open(pd, 'w', encoding='utf-8') as file:
                RD.write(file)  # 数据写入配置文件
            self.destroy()  # 销毁窗口
        else:
            self.msg.set('没有图片!')
##########################################################################

class Photo(tk.Toplevel):
    # 图片查看
    def __init__(self, parent):
        super().__init__()
        self.title('查看图片')
        self.parent = parent  # 显式地保留父窗口
        self.setupUI()


    def setupUI(self):

        img_pwd = RD.get('HTTP', 'img_pwd')
        # print(os.path.isfile(img_pwd))
        # self.attributes("-toolwindow", 1)
        # self.wm_attributes("-topmost", 1)
        row1 = tk.Frame(self)
        row1.pack(fill='x')
        self.img = Image.open(img_pwd)
        (h, w) = self.img.size
        if h > 1080 or w > 1080:
            self.img = self.img.resize((int(h / 2), int(w / 2)),
                                    Image.ANTIALIAS)  #图片尺寸调整
        self.photo = ImageTk.PhotoImage(self.img)  #在root实例化创建，否则会报错
        label = tk.Label(row1, image=self.photo)
        label.pack()


##########################################################################
class Run_JS(tk.Toplevel):
    # 批量复制
    def __init__(self, parent):
        super().__init__()
        self.title('批量复制生成')

        # self.geometry('450x450')
        
        self.parent = parent  # 显式地保留父窗口
        self.setupUI()

    def setupUI(self):

        row1 = tk.Frame(self,bg='#AFEEEE')
        row1.pack(fill='x')
        tk.Label(row1,text='基础数据',bg='#AFEEEE').grid(row=1,column=1,sticky='w')
        self.Raw_data = tk.Text(row1,width=50,height=10,bd=5)
        self.Raw_data.grid(row=2,column=1,sticky='w')


        row2 = tk.Frame(self,bg='#AFEEEE')
        row2.pack(fill='x')
        tk.Label(row2,text='行',bg='#AFEEEE').pack(side=tk.LEFT)

        self.Raw_line = tk.StringVar(value='1')  #输入框
        tk.Entry(row2,width=50, textvariable=self.Raw_line, bd=5).pack(side=tk.LEFT)


        row3 = tk.Frame(self,bg='#AFEEEE')
        row3.pack(fill='x')
        tk.Label(row3,text='列',bg='#AFEEEE').pack(side=tk.LEFT)
        
        self.Raw_list = tk.StringVar(value='1')  #输入框
        tk.Entry(row3,width=50, textvariable=self.Raw_list, bd=5).pack(side=tk.LEFT)

        row4 = tk.Frame(self,bg='#AFEEEE')
        row4.pack(fill='x')
        tk.Label(row4,text='列表矫正处理：',bg='#AFEEEE').pack(side=tk.LEFT)


        row5 = tk.Frame(self,bg='#AFEEEE')
        row5.pack(fill='x')
        tk.Label(row5,text='行矫正：',bg='#AFEEEE').pack(side=tk.LEFT)

        tk.Label(row5,text='每行增加',bg='#AFEEEE').pack(side=tk.LEFT)
        self.Raw_line1 = tk.StringVar(value='1')  #输入框
        tk.Entry(row5,width=3, textvariable=self.Raw_line1, bd=5).pack(side=tk.LEFT)

        tk.Label(row5,text='======每隔',bg='#AFEEEE').pack(side=tk.LEFT)
        self.Raw_line2 = tk.StringVar(value='1')  #输入框
        tk.Entry(row5,width=3, textvariable=self.Raw_line2, bd=5).pack(side=tk.LEFT)
        tk.Label(row5,text='行减',bg='#AFEEEE').pack(side=tk.LEFT)
        self.Raw_line3 = tk.StringVar(value='1')  #输入框
        tk.Entry(row5,width=3, textvariable=self.Raw_line3, bd=5).pack(side=tk.LEFT)

        row6 = tk.Frame(self,bg='#AFEEEE')
        row6.pack(fill='x')
        tk.Label(row6,text='列矫正：',bg='#AFEEEE').pack(side=tk.LEFT)
        tk.Label(row6,text='每列增加',bg='#AFEEEE').pack(side=tk.LEFT)
        self.Raw_list1 = tk.StringVar(value='1')  #输入框
        tk.Entry(row6,width=3, textvariable=self.Raw_list1, bd=5).pack(side=tk.LEFT)

        tk.Label(row6,text='======每隔',bg='#AFEEEE').pack(side=tk.LEFT)
        self.Raw_list2 = tk.StringVar(value='1')  #输入框
        tk.Entry(row6,width=3, textvariable=self.Raw_list2, bd=5).pack(side=tk.LEFT)
        tk.Label(row6,text='列减',bg='#AFEEEE').pack(side=tk.LEFT)
        self.Raw_list3 = tk.StringVar(value='1')  #输入框
        tk.Entry(row6,width=3, textvariable=self.Raw_list3, bd=5).pack(side=tk.LEFT)

        row7 = tk.Frame(self,bg='#AFEEEE')
        row7.pack(fill='x')
        tk.Button(row7,text="开始执行",width=20,height=4,bd=5,command=self.search).pack(side=tk.BOTTOM)


    def search(self):
        a = eval(self.Raw_data.get(0.0,tk.END))
        print(self.Raw_line.get().split(','))
        print(self.Raw_list.get().split(','))
        unit_name = 0 #名称
        jieguo = []
        for name in a:
            #循环原始列表
            #获取需要改变的数据
            height = int(copy.deepcopy(name.get('height')))
            width = int(copy.deepcopy(name.get('width')))
            top = int(copy.deepcopy(name.get('top')))
            left = int(copy.deepcopy(name.get('left')))
            # 获取当前执行的块需要循环多少行列。
            dy_hang = self.Raw_line.get().split(',').pop(0)
            dy_lie = self.Raw_list.get().split(',').pop(0)
            for i in range(int(dy_hang)):
                #一级循环
                #循环完成一行后，需要重置一次列
                lefts = left
                # 当前行位置加上块高度
                for a in range(int(dy_lie)):
                    #二级循环
                    name["top"] = "%s"%(top)
                    name["left"] = "%s"%(lefts)
                    name["name"] = "Rect%s"%(unit_name)
                    unit_name+=1
                    jieguo.append(copy.deepcopy(name))
                    # print(name.items())
                    # 循环一次增加一次列的距离，
                    lefts+=width+(int(self.Raw_list3.get()) if a%int(self.Raw_list2.get())  else int(self.Raw_list1.get()))
                top = '%s'%(int(name.get('top'))+height+(int(self.Raw_line3.get()) if i%int(self.Raw_line2.get())  else int(self.Raw_line1.get())))


        # 推送到服务器
        jieguo = re.sub("'",'"','%s'%jieguo)
        payload = {
            "userId":RD.get('USER', 'userid'),
            "token": RD.get('USER', 'token'),
            "brokeId": RD.get('USER', 'brokeid'),
            "sitePlanId": RD.get('SITEPLAN', 'siteplanid'),
            "content": jieguo
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        ret = requests.post(RD.get('HTTP', 'none_url')+RD.get('HTTP', 'updatesitecontent'), data=payload)
        self.r = ret.json()
        print(self.r)
        self.destroy()  # 销毁窗口
        return '1'


##########################################################################

# 主窗
class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.pack() # 若继承 tk.Frame ，此句必须有！
        self.title('自动画图工具')
        # self.geometry('550x450')
        # self.setup_config()
        # self.iconbitmap('spider_128px_1169260_easyicon.net.ico')
        self.setupUI()

    def setupUI(self):

        self.img = Image.open(r'.\IMGS\a03.png')
        self.photo = ImageTk.PhotoImage(self.img)  #在root实例化创建，否则会报错
        label = tk.Label(self,image=self.photo,bg='#AFEEEE')
        label.pack()
        
        
        row1 = tk.Frame(self,bg='#AFEEEE')
        row1.pack(fill="x")
        self.user_names = tk.IntVar(value='登录')
        tk.Button(row1,textvariable=self.user_names,width=20,height=3,bd=5,command=self.go_loging).pack(side=tk.LEFT)
        # self.user_names = tk.IntVar(value=RD.get('USER', 'username'))
        # tk.Label(
        #     row1, textvariable=self.user_names, width=10,bg='#AFEEEE').pack(side=tk.LEFT)

        #选择项目
        # row2 = tk.Frame(self,bg='#AFEEEE')
        # row2.pack(fill="x")
        self.project_name = tk.IntVar(value='选择项目')
        tk.Button(row1,textvariable=self.project_name,width=20,height=3,bd=5,command=self.go_project).pack(side=tk.LEFT)

        # self.project_name = tk.IntVar(value=RD.get('PROJECT', 'projectname'))
        # tk.Label(
        #     row2, textvariable=self.project_name,bg='#AFEEEE').pack(side=tk.LEFT)


        #选择building
        row3 = tk.Frame(self,bg='#AFEEEE')
        row3.pack(fill="x")
        self.buildings = tk.IntVar(value='选择building')
        tk.Button(row1,textvariable=self.buildings,width=20,height=3,bd=5,command=self.go_siteplan).pack(side=tk.LEFT)
        # 图片查看
        tk.Label(row3,text='图片路径：',bg='#AFEEEE').pack(side=tk.LEFT)
        self.TPM = tk.IntVar(value=RD.get('HTTP', 'img_pwd'))
        tk.Label(
            row3, textvariable=self.TPM,bg='#AFEEEE').pack(side=tk.LEFT)
        tk.Button(
            row3, text="查看图片", width=6, height=1, bd=5,
            command=self.img_look).pack(side=tk.LEFT)
        # 执行画图工具
        row4 = tk.Frame(self,bg='#AFEEEE')
        row4.pack(fill="x")

        
        tk.Label(row4,text='是否去除表头：',bg='#AFEEEE').pack(side=tk.LEFT)

        self.heads = tk.IntVar()
        self.heads.set(1)
        check = tk.Checkbutton(row4,
        text='',
        variable = self.heads,
        onvalue =1,
        offvalue=2,bg='#AFEEEE'
        )
        check.pack(side=tk.LEFT)



        row5 = tk.Frame(self,bg='#AFEEEE')
        row5.pack(fill="x")
        tk.Button(row5,text="画图",width=20,height=3,bd=5,command=self.RUN).pack(side=tk.LEFT)
        tk.Button(row5,text="复制",width=20,height=3,bd=5,command=self.run_ts).pack(side=tk.LEFT)
        self.retn = tk.IntVar(value='')
        tk.Label(row5,textvariable=self.retn,bg='#AFEEEE',fg='red').pack(side=tk.LEFT)

    def go_loging(self):
        # 接收弹窗的数据
        res = self.ask_userinfo()
        self.user_names.set(RD.get('USER', 'username'))
        
    def ask_userinfo(self):
        # 登录弹窗
        inputDialog = MyDialog(self)
        self.wait_window(inputDialog)  # 这一句很重要！！！
        return inputDialog


    
    def go_project(self):
        #处理项目列表
        res = self.get_pro()
        self.project_name.set(RD.get('PROJECT', 'projectname'))
    def get_pro(self):
        #获取项目弹窗
        project = Project(self)
        self.wait_window(project)  # 这一句很重要！！！
        return project


    def go_siteplan(self):
        # 获取siteplan列表
        res = self.get_siteplans()
        self.buildings.set(RD.get('SITEPLAN','siteplanname'))
        self.TPM.set(RD.get('HTTP','img_pwd'))
    def get_siteplans(self):
        # siteplan选择弹窗
        siteplan = BuildDing(self)
        self.wait_window(siteplan)  # 这一句很重要！！！
        return siteplan

    def img_look(self):
        # 查看图片
        img_pwd = RD.get('HTTP', 'img_pwd')
        # print(os.path.isfile(img_pwd))
        if os.path.isfile(img_pwd):
            imgs = Photo(self)
            self.wait_window(imgs)
            self.TPM.set(img_pwd)
        else:
            self.TPM.set('图片不存在！！')

    def run_ts(self):
        # 批量复制
        res = self.run_json()
        print(res)
        if res['code'] == '0':
            self.retn.set('创建成功！！')
        else:
            
            self.retn.set('创建失败：%s'%res['msg'])

    def run_json(self):
        # 复制模块
        run_js = Run_JS(self)
        self.wait_window(run_js)  # 这一句很重要！！！
        print(run_js.r)
        return run_js.r

##################################################################################################

    def RUN(self):
        # 图片识别
        img_pth = RD.get('HTTP','img_pwd')
        image=cv2.imdecode(np.fromfile(img_pth,dtype=np.uint8),-1) # 中文路径问题解决
        # 二值化
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(~gray, 255,
                                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, -1)
        rows, cols = binary.shape
        scale = 80
        # 识别横线
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
        eroded = cv2.erode(binary, kernel, iterations=1)
        dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
        # 识别竖线
        scale = 5
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
        eroded1 = cv2.erode(binary, kernel, iterations=1)
        dilatedrow = cv2.dilate(eroded1, kernel, iterations=1)
        # 标识表格
        merge = cv2.add(dilatedcol, dilatedrow)
        # #获取交点
        bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)

        ys, xs = np.where(bitwiseAnd > 0)
        ll = [ (xs[i],ys[i]) for i in range(len(ys))] #获取交点)
        #  findContours 获取轮廓
        contours, hierarchy = cv2.findContours(merge, cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image,contours,-1,(0,0,255),2)
        cv2.imshow("add Image", image)
        cv2.waitKey(0)
        content = []
        name = 0
        mean_size = np.mean([cv2.contourArea(i) for i in contours])  #获取平均面积
        
        for i, contour in enumerate(contours):
            f = 0
            x, y, w, h = cv2.boundingRect(contour)
            size = cv2.contourArea(contour)  #获取面积
            if self.heads.get() == 1 :
                for i in ll:
                    if 0 <= int(x-i[0])<= 10 and 0 <= int(y-i[1])<= 10 :
                        f = 1
                        break
            else:
                f = 1
            if f != 0 and  1 < size < mean_size*2:
                mb = {
                    "width": "%s" % (w - 2),
                    "height": "%s" % (h - 2),
                    "left": "%s" % (x + 1),
                    "top": "%s" % (y + 1),
                    "name": "Rect%s" % name,
                    "fill": "rgba(220,20,60,0.4)",
                    "type": "rect"
                }
                content.append(mb)
                name += 1


        # 推送到服务器
        content = re.sub("'", '"', '%s' % content)  # 将单引号换成双引号
        content = re.sub("\n", '', '%s' % content)  # 去除换行符
        payload = {
            "userId":RD.get('USER', 'userid'),
            "token": RD.get('USER', 'token'),
            "brokeId": RD.get('USER', 'brokeid'),
            "sitePlanId": RD.get('SITEPLAN', 'siteplanid'),
            "content": content
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        ret = requests.post(RD.get('HTTP', 'none_url')+RD.get('HTTP', 'updatesitecontent'), data=payload)
        r = ret.json()
        # print(r)
        if r['code'] == '0':
            self.retn.set('创建成功！！')
        else:
            
            self.retn.set('创建失败：%s'%r['msg'])
        return r








if __name__ == '__main__':
    app = MyApp()
    app.mainloop()