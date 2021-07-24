# 公用函数，数据库读写，配置文件读取

import math
import time
import random
import json
import math
import time
import random
import wave
import numpy as np
from scipy import signal
import pymysql
from sshtunnel import SSHTunnelForwarder
import time
import requests
import os
import cv2

def generateBlackVideo():
    output_filename="../data/media/black.hd.avi"
    output_video_filename="../data/media/black.onlyvideo.avi"
    cv_writer=cv2.VideoWriter(output_video_filename,cv2.VideoWriter_fourcc(*'XVID'),24,(320,180),True)

    n_frame=24*60

    frame = [[[0]*3]*320]*180
    f=np.array(frame,np.uint8)
    for i in range(n_frame):
        cv_writer.write(f)
    cv_writer.release()

    output_audio_filename = "../data/media/black.onlyaudio.mp3"
    fp = wave.Wave_write(output_audio_filename)
    framerate = 44100
    time = 60
    t = np.arange(0, time, 1.0/framerate)
    wave_data = signal.chirp(t, 100, time, 1000, method='linear') * 10000
    wave_data = wave_data.astype(np.short)

    fp.setframerate(44100)
    fp.setnframes(60*44100)
    fp.setnchannels(1)
    fp.setsampwidth(2)
    fp.writeframes(wave_data.tostring())
    fp.close()

    cmd = 'ffmpeg -i %s -i %s %s'%(output_video_filename,output_audio_filename,output_filename)
    os.system(cmd)

def readVideo(videoname):
    capture = cv2.VideoCapture(videoname )
    ans=[]
    if capture.isOpened():
        while True:
            ret,img=capture.read() # img 就是一帧图片        
            ans.append(img)
            if not ret:break # 当获取完最后一帧就结束
    else:
        print('readVideo: 视频打开失败！')
    return ans


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
    db = pymysql.connect(
        host=readConfig("mysql_host"),  # 映射地址local_bind_address IP
        port=readConfig("mysql_port"),  # 映射地址local_bind_address端口
        user=readConfig("mysql_user"),
        passwd=readConfig("mysql_password"),
        database=DB, 
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor if isDict==True else pymysql.cursors.Cursor)
    cursor = db.cursor()
    cursor.execute(SQL.encode('utf8')) 
    data = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return data


def query(DB, SQL, isDict=False, isRemote=False):
    return SSHMysql(DB, SQL, isDict=isDict, isRemote=isRemote)


def sqlQuery(sql, isDict=False):
    return query(readConfig("dbname"),sql,isDict=isDict)

def readConfig(key, filename="config.json"):
    f=open(filename, "r")
    obj=json.load(f)
    f.close()
    return obj[key]

def getFileList(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files


def getBinaryFile(filename):
	f = open(filename, "rb")
	data = f.read()
	f.close()
	return data

def generateXvid():
    return "XV"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)

def generateCutid():
    return "CT"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)

def generateOvid():
    return "OV"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)


def generateTempid():
    return "T"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)


# 给定二值化后的波形，提取时长合法的片段并计算总长
# 您不需要关心该函数的具体实现
def makeRanges(bans, lim_min, lim_max):
    ans=[]
    length=len(bans)
    last=-2
    now=0
    tot=0
    for i in range(length):
        if bans[i]>0:
            if i==now+1:
                now=i
            else: 
                if last>-2:
                    dura=now-last
                    if lim_min<dura and dura<lim_max:
                        ans+=[[last,now]]
                        tot+=now-last
                    last=-2
                else:
                    last=i
                    now=i
    return ans, tot

def conf(key):
    return readConfig(key)

def wstat(id, s, ext=False):
    sqlQuery("insert into status (id, p, ext) values ('%s',%d,%d);" %(id,s,1 if ext else 0))