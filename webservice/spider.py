import sys
sys.path.append("..")

import os
import re
import json
import re
import json
import requests
import pymysql
import sys
import common
import sshtunnel
import random
from threading import Thread


def importMP4(video_id, input_filename):
    common.wstat(video_id,0+random.randint(0,10))

    ffmpeg_config=common.readConfig("ffmpeg_hd")
    os.system('ffmpeg -y -i ' + input_filename + ' ' + ffmpeg_config + ' ../data/media/'+video_id+'.hd.mp4  -hide_banner -loglevel error')

    common.wstat(video_id,50+random.randint(0,30))

    ffmpeg_config=common.readConfig("ffmpeg_ld")
    os.system('ffmpeg -y -i ' + input_filename + ' ' + ffmpeg_config + ' ../data/media/'+video_id+'.mp4  -hide_banner -loglevel error')


cookie = r"_uuid=FE18E94F-CAB1-69C0-753C-245A94DB063C04672infoc; buvid3=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|RYJYllJY0J'uY|ukYlm||; buivd_fp=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; buvid_fp_plain=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; buvid_fp=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; DedeUserID=471644009; DedeUserID__ckMd5=bf15e248b5d4efa0; SESSDATA=310ee312,1639652841,6e913*61; bili_jct=d9b1b1df5c76395cf9d321ab48a3c41d; sid=6wmbwi63; fingerprint3=7cdce1880b09344ee0d74616931713d7; fingerprint=a6ec6277365ffa20b8973976cadc42f0; fingerprint_s=193f3299bcb4e2c36d107cd3a0b51a14; CURRENT_QUALITY=112; bp_video_offset_471644009=542730492934997055; bp_t_offset_471644009=542734418540372470; bsource=search_baidu; bfe_id=6f2695e1895fb89897286b11ddc486b0; PVID=3"


def GetHTMLContent(url, cookie=''):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Cookie': cookie
    }
    response = requests.get(url, headers=headers)
    return response.content.decode("utf-8")


def GetBidsBySearch(searchKeyword, page=1):
    urlSearch = "https://search.bilibili.com/all?keyword=" + \
        searchKeyword+"&from_source=web_search&page=" + str(page) + "&duration=1" # 测试阶段，限制下长度
    htmlSearch = GetHTMLContent(urlSearch)
    reBid = re.compile(r'//www.bilibili.com/video/(.*?)\?from=search')
    listBid = re.findall(reBid, htmlSearch)
    return listBid


def GetDanmuFromXml(list, cid):
    reDanmu = re.compile(
        r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>')
    listDanmu = re.findall(reDanmu, list)
    listDictDanmu = []
    for itemDanmu in listDanmu:
        # 去除高级弹幕

        if itemDanmu[8] == '':
            continue
        if itemDanmu[8][0] == '[':
            continue
        dictItemDanmu = {}
        dictItemDanmu["cid"] = cid
        dictItemDanmu["floattime"] = float(itemDanmu[0])
        dictItemDanmu["mode"] = itemDanmu[1]
        dictItemDanmu["size"] = itemDanmu[2]
        dictItemDanmu["color"] = itemDanmu[3]
        dictItemDanmu["timestamp"] = itemDanmu[4]
        dictItemDanmu["pool"] = itemDanmu[5]
        dictItemDanmu["author"] = itemDanmu[6]
        dictItemDanmu["rowid"] = itemDanmu[7]
        dictItemDanmu["text"] = itemDanmu[8]
        listDictDanmu += [dictItemDanmu]
    return listDictDanmu


def GetVInfoFromResponse(response):
    objVInfo = {}
    data = json.loads(response)['data']
    # 基本信息

    objVInfo['aid'] = data['aid']  # 视频ID

    objVInfo['bvid '] = data['bvid']  # 视频ID
    objVInfo['cid'] = data['cid']  # 弹幕连接id
    objVInfo['tid '] = data['tid']  # 区
    objVInfo['iscopy'] = data['copyright']  # 是否转载
    objVInfo['tname'] = data['tname']  # 子分区
    objVInfo['pic'] = data['pic']  # 封面
    objVInfo['title'] = data['title']  # 标题
    objVInfo['descs'] = data['desc']  # 简介
    objVInfo['duration'] = data['duration']  # 总时长，所有分P时长总和
    objVInfo['dimension'] = str(data['dimension'])  # 视频1P分辨率
    objVInfo['videos'] = data['videos']  # 分P数
    objVInfo['pubdate'] = data['pubdate']  # 发布时间
    objVInfo['ctime'] = data['ctime']  # 用户投稿时间

    # 视频状态
    stat = data['stat']

    objVInfo['view'] = stat['view']  # 播放数
    objVInfo['danmaku'] = stat['danmaku']   # 弹幕数
    objVInfo['reply'] = stat['reply']   # 评论数
    objVInfo['likes'] = stat['like']   # 点赞数
    objVInfo['dislikes'] = stat['dislike']   # 点踩数
    objVInfo['coin'] = stat['coin']   # 投币数
    objVInfo['favorite'] = stat['favorite']   # 收藏数
    objVInfo['share '] = stat['share']  # 分享数
    objVInfo['now_rank'] = stat['now_rank']  # 当前排名
    objVInfo['his_rank'] = stat['his_rank']  # 历史最高排名

    owner = data['owner']
    objVInfo['mid'] = owner['mid']  # UP主ID

    return objVInfo, objVInfo['aid']


def GetRlistByResponse(response):
    ReplyList = []
    RepliList = json.loads(response)['data']['replies']

    for Repli in RepliList:
        objRepli = {}
        objRepli['oid'] = Repli['oid']
        objRepli['message'] = Repli['content']['message']
        objRepli['mid'] = Repli['mid']
        objRepli['likes'] = Repli['like']
        objRepli['ctime'] = Repli['ctime']
        objRepli['rpid'] = Repli['rpid']

        ReplyList.append(objRepli)
    return ReplyList


def GetDanmuByCid(queryCid):
    urlDanmuXml = 'https://comment.bilibili.com/'+queryCid+'.xml'
    strDanmuXml = GetHTMLContent(urlDanmuXml)
    danmu = GetDanmuFromXml(strDanmuXml, queryCid)
    return danmu


def GetCidByBid(queryBid):
    urlGetCid = "https://api.bilibili.com/x/player/pagelist?bvid=" + \
        queryBid + "&jsonp=jsonp"
    strCidJson = GetHTMLContent(urlGetCid)
    jsonCid = json.loads(strCidJson)

    return str(jsonCid["data"][0]["cid"])


def GetDanmuByBid(bvid):
    queryCid = GetCidByBid(bvid)
    Danmulist = GetDanmuByCid(queryCid)
    return Danmulist


def GetVInfoByBid(bvid):

    url = r'http://api.bilibili.com/x/web-interface/view?bvid={}'.format(bvid)
    response = GetHTMLContent(url)
    VInfo = GetVInfoFromResponse(response)
    return VInfo


def GetVReplyByOid(oid, cookie, Type=1, ps=49, pn=1):
    url = r'http://api.bilibili.com/x/v2/reply?type={}&oid={}&pn={}&ps={}'.format(
        Type, oid, pn, ps)
    response = GetHTMLContent(url, cookie)
    ReplyList = GetRlistByResponse(response)

    return ReplyList


def InsertVInfo(data,cursor,conn):
    # data = dict(item)
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'insert ignore into %s (%s) values (%s)' % ('Vinfo', keys, values)
    cursor.execute(sql, tuple(data.values()))
    conn.commit()


def InsertDanmu(datas,cursor,conn):
    # data = dict(item)
    if len(datas)==0:
        return
    keys = ', '.join(datas[0].keys())
    values = ', '.join(['%s'] * len(datas[0]))
    sql = ('insert ignore into %s (%s) values (%s);' % ('Danmu', keys, values))
    ls=[]
    for data in datas:
        ls.append(tuple(data.values()))
    cursor.executemany(sql, ls)
    conn.commit()


def GetAllInfoByBid(vbid):
    DanmuList = GetDanmuByBid(vbid)
    VInfoObj, oid = GetVInfoByBid(vbid)
    return DanmuList, VInfoObj

def getInfo(vbid,MYSQL_DBNAME=common.readConfig("dbname"),MYSQL_HOST=common.readConfig("mysql_host"),MYSQL_USER=common.readConfig("mysql_user"),
MYSQL_PASSWD=common.readConfig("mysql_password"),MYSQL_PORT=common.readConfig("mysql_port")):
    conn = pymysql.connect(
        host=MYSQL_HOST,  # 映射地址local_bind_address IP
        port=MYSQL_PORT,  # 映射地址local_bind_address端口
        user=MYSQL_USER,
        passwd=MYSQL_PASSWD,
        database=MYSQL_DBNAME,  # 需要连接的实例名
        charset='utf8')
    cursor = conn.cursor()
    DanmuList,VInfoObj=GetAllInfoByBid(vbid)
    InsertVInfo(VInfoObj,cursor,conn)
    InsertDanmu(DanmuList,cursor,conn)
    cursor.close()
    conn.close()
    return VInfoObj


def getMP4(video_id):
    common.wstat(video_id,0)

    pageUrl = "https://www.bilibili.com/video/" + video_id
    htmlText = common.getRequestsText(pageUrl, pageUrl)
    urlJson = json.loads(re.findall(
        '<script>window\.__playinfo__=(.*?)</script>', htmlText)[0])

    videoUrl = urlJson['data']['dash']['video'][0]['backupUrl'][0]
    audioUrl = urlJson['data']['dash']['audio'][0]['backupUrl'][0]

    common.wstat(video_id,1+random.randint(0,5))

    audioFile = common.getRequestsContent(audioUrl, pageUrl)
    with open('../tmp/audio_'+video_id+'.mp3', 'wb') as f:
        f.write(audioFile)
    common.wstat(video_id,10+random.randint(0,10))
    videoFile = common.getRequestsContent(videoUrl, pageUrl)
    with open('../tmp/video_'+video_id+'.mp4', 'wb') as f:
        f.write(videoFile)

    common.wstat(video_id,50+random.randint(0,30))

    def A():
        ffmpeg_config=common.readConfig("ffmpeg_hd")
        os.system('ffmpeg -y -i ../tmp/video_'+video_id+'.mp4 -i ../tmp/audio_' +
                video_id+'.mp3 ' + ffmpeg_config + ' ../data/media/'+video_id+'.hd.mp4  -hide_banner -loglevel error')
    def B():
        ffmpeg_config=common.readConfig("ffmpeg_ld")
        os.system('ffmpeg -y -i ../tmp/video_'+video_id+'.mp4 -i ../tmp/audio_' +
                video_id+'.mp3 ' + ffmpeg_config + ' ../data/media/'+video_id+'.mp4  -hide_banner -loglevel error')
    
    thread_handles=[]
    thread_handles.append(Thread(target=A))
    thread_handles.append(Thread(target=B))
    for th in thread_handles: th.start()
    for th in thread_handles: th.join()

    common.wstat(video_id,100)
    
####################################################

# 如果 bv 信息不存在，则下载 bv 信息
def downloadInfo(bvid):
    ans = common.query(
        common.readConfig("dbname"), "select * from Vinfo where bvid='%s'" % bvid)
    if len(ans) > 0:
        print("  spider: Info already exists. Terminated.", bvid)
        return
    getInfo(bvid)

# 拉取 bv 
def downloadMedia(bvid):
    getMP4(bvid)

# 导入本地媒体，filename 为文件路径
def importMedia(bvid, filename):
    if os.path.isfile(filename) == False:
        print("  spider: Source media invalid. Terminated.", bvid)
    importMP4(bvid, filename)

# 获取搜索结果（第一页）
def getSearchResult(keyword):
    return GetBidsBySearch(keyword)