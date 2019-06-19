import cv2
import re
import requests
import pytesseract
import numpy as np
from urllib.parse import quote
from PIL import Image
from aip import AipImageClassify
import configparser
import json



pd = R'E:\新联国际\地产项目\自动画图\HUATU\config.ini'
RD = configparser.ConfigParser()
RD.read(pd, encoding='utf-8')

# 请求参数



print(img_pth)

class Run_HT():
    def __init__(self):
        pass


    def RUN(self):
        
        # image = cv2.imread(img_pth, 1)
        image=cv2.imdecode(np.fromfile(img_pth,dtype=np.uint8),-1) # 中文路径问题解决
        print(image)
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
        # cv2.imshow("add Image", dilatedcol)
        # cv2.waitKey(0)
        # 识别竖线
        scale = 5
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
        eroded1 = cv2.erode(binary, kernel, iterations=1)
        dilatedrow = cv2.dilate(eroded1, kernel, iterations=1)
        # cv2.imshow("add Image", dilatedrow)
        # cv2.waitKey(0)
        # 标识表格
        merge = cv2.add(dilatedcol, dilatedrow)
        # cv2.imwrite(R'new_img.jpg', merge)  # 将得到的表格图片储存
        # cv2.imshow("add Image", merge)
        # cv2.waitKey(0)

        # #获取交点
        bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)

        ys, xs = np.where(bitwiseAnd > 0)
        ll = [(xs[i], ys[i]) for i in range(len(ys))]  #获取交点)

        # # 二次处理
        # image1 = cv2.imread(R'new_img.jpg', 1)
        # gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        # binary = cv2.adaptiveThreshold(~gray, 255,
        #                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                cv2.THRESH_BINARY, 11, 2)
        # ret, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        #  findContours 获取轮廓
        contours, hierarchy = cv2.findContours(merge, cv2.RETR_LIST,
                                               cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(image,contours,-1,(0,0,255),2)
        cv2.imshow("add Image", image)
        cv2.waitKey(0)
        content = []
        name = 0
        mean_size = np.mean([cv2.contourArea(i) for i in contours])  #获取平均面积
        f = 0
        # print(len(contours))
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            size = cv2.contourArea(contour)  #获取面积
            for i in ll:
                if 0 <= int(x - i[0]) <= 10 and 0 <= int(y - i[1]) <= 10:
                    f = 1
                    break
            if f != 0 and 1 < size < mean_size:
                mb = {
                    "width": "%s" % (w - 2),
                    "height": "%s" % (h - 2),
                    "left": "%s" % (x + 1),
                    "top": "%s" % (y + 1),
                    "name": "Rect%s" % name,
                    "fill": "rgba(220,20,60,0.4)",
                    "type": "rect"
                }
                # print(mb)
                content.append(mb)
                name += 1
            elif f == 0:
                pass
                # print(y,y+w,x,x+w-w)

        # 推送到服务器
        content = re.sub("'", '"', '%s' % content)  # 将单引号换成双引号
        content = re.sub("\n", '', '%s' % content)  # 去除换行符
        # content = quote('%s' % content, 'utf-8')  # 转码
        payload = {
            "userId":RD.get('USER', 'userid'),
            "token": RD.get('USER', 'token'),
            "brokeId": RD.get('USER', 'brokeid'),
            "sitePlanId": RD.get('SITEPLAN', 'siteplanid'),
            "content": content
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        ret = requests.post(RD.get('HTTP', 'none_url')+RD.get('HTTP', 'updatesitecontent'), data=payload)
        return ret.json()
        

