import requests
import configparser

pd = R'E:\新联国际\地产项目\自动画图\HUATU\config.ini'
RD = configparser.ConfigParser()
RD.read(pd, encoding='utf-8')



# def login(url, user_email, User_password):
#     data={
#                 'userId': '',
#                 'token': '',
#                 'brokeId': '',
#                 'email': user_email,
#                 'password': User_password
#             }
#     userss = requests.post(url,data = data)
#     print(userss)
#     return userss

# print(RD.get('USER', 'userid'))
# data = {
#     'userId': '6',
#     'token': 'cdbce93709364e84a22617ad3c359eb0',
#     'brokeId': '0c5d80359cc5416a9ea953fdebcbfc20',
#     'pageSize': '50',
#     'pageNo': '1',
#     'projectName': '10'
# }
# project = requests.get(
#     RD.get('HTTP', 'url2') + RD.get('HTTP', 'queryproject'),
#     params=data).json()
# # print(project['datas']['lists'])
# for i in project['datas']['lists'] :
#     print(i)

