import math
import time
import random
import json
import math
import time
import random

import pymysql
from sshtunnel import SSHTunnelForwarder
import time
import requests


def getRequestsContentUtf8(url, referee=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).content.decode("utf-8")


def getRequestsText(url, referee=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).text


def getRequestsContent(url, referee=""):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'Referer': referee
    }
    return requests.get(url, headers=headers).content
    
def SSHMysql(DB, SQL, isDict=False, isRemote=False):
    flag=0
    data=[]
    for i in range(50):
        # print(">",end='')
        try:
            if isRemote==True:
                server = SSHTunnelForwarder(
                    ssh_address_or_host=('131.mollnn.com', 22),  # 指定ssh登录的跳转机的address
                    ssh_username='wzc',  # 跳转机的用户
                    ssh_password='123456',  # 跳转机的密码
                    local_bind_address=('127.0.0.1', 1268),  # 映射到本机的地址和端口
                    remote_bind_address=('localhost', 3306))  # 数据库的地址和端口
                server.start()  # 启用SSH
                db = pymysql.connect(
                    host="127.0.0.1",  # 映射地址local_bind_address IP
                    port=1268,  # 映射地址local_bind_address端口
                    user="root",
                    passwd="123456",
                    database=DB, 
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor if isDict==True else pymysql.cursors.Cursor)
                cursor = db.cursor()
                cursor.execute(SQL.encode('utf8')) 
                data = cursor.fetchall()
                cursor.close()
                db.commit()
                db.close()
                server.close()
            else:
                db = pymysql.connect(
                    host="127.0.0.1",  # 映射地址local_bind_address IP
                    port=3306,  # 映射地址local_bind_address端口
                    user="root",
                    passwd="123456",
                    database=DB, 
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor if isDict==True else pymysql.cursors.Cursor)
                cursor = db.cursor()
                cursor.execute(SQL.encode('utf8')) 
                data = cursor.fetchall()
                cursor.close()
                db.commit()
                db.close()
            break
        except Exception:
            flag=0
        else:
            flag=0
        time.sleep(0.5)
    # print("end")
    return data


def query(DB, SQL, isDict=False, isRemote=False):
    return SSHMysql(DB, SQL, isDict=isDict, isRemote=isRemote)


def readConfig(key, filename="config.json"):
    f=open(filename, "r")
    obj=json.load(f)
    f.close()
    return obj[key]

def generateXvid():
    return "XV"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)

def generateCutid():
    return "CT"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)