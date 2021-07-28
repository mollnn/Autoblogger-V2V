from posix import times_result

from numpy import single
import common
import spider
import os
from common import sqlQuery
import extractor
import generator
import publisher
import time
from threading import Thread
from common import conf

# 下载一个视频
def singleDownload(bvid):
    print("single download",bvid)
    spider.downloadInfo(bvid)
    spider.downloadMedia(bvid)

# 导入一个视频
def singleImport(bvid):
    spider.downloadInfo(bvid)   # 下载 vinfo+danmu 不怎么吃资源就现场下载好了
    spider.importMedia(bvid)

def singleExtract(bvid):
    extractor.main(bvid)

# 下载一个视频 + 提取
def bondDownloadExtract(bvid):
    print("bond download",bvid)
    spider.downloadInfo(bvid)
    spider.downloadMedia(bvid)
    extractor.main(bvid)


def singleGenerate(description, tag):
    generator.main(description, tag)


def singlePublish(ovid):
    publisher.publish(ovid)

def clearDatafile():
    os.system("rm ../data/media/*.mp4 -rf")
    os.system("rm ../data/edited/*.mp4 -rf")
    os.system("rm ../data/output/*.mp4 -rf")
    os.system("rm ../data/poster/*.jpg -rf")

def execute():
    clearDatafile()
    sqlQuery("truncate table vinfo")
    sqlQuery("truncate table danmu")
    sqlQuery("truncate table extraction")
    sqlQuery("truncate table edition")
    sqlQuery("truncate table status")
    sqlQuery("truncate table out_info")
    
    in_src=sqlQuery("select * from in_src")
    in_gen=sqlQuery("select * from in_gen")

    lt=time.time()

    download_list=[]
    down_src_list=[]
    down_gen_list=[]
    for i in in_src:
        if i[0] not in download_list: 
            download_list.append(i[0])
            down_src_list.append(i[0])
    for i in in_gen: 
        if len(i[0])>2 and i[0][0:2]=="BV" and i[0] not in download_list:
            download_list.append(i[0])
            down_gen_list.append(i[0])

    thread_handles=[]
    for i in down_src_list:
        thread_handles.append(Thread(target=bondDownloadExtract, args=(i,)))
        common.wstat(i,0,ext=False)
        common.wstat(i,0,ext=True)

    for i in down_gen_list: 
        thread_handles.append(Thread(target=singleDownload, args=(i,)))
        common.wstat(i,0,ext=False)

    for th in thread_handles: 
        th.start()
        time.sleep(0.2)  # 防止请求并发度过大
    for th in thread_handles:
        th.join()

    thread_handles=[]
    for i in in_gen: 
        thread_handles.append(Thread(target=singleGenerate, args=(i[0], int(i[1]),)))
    for th in thread_handles: 
        th.start()
    for th in thread_handles:
        th.join()

    print("----- total",time.time()-lt)

    out_list = sqlQuery("select ovid from out_info")
    flag=0
    for i in out_list:
        if flag==1:
            for j in range(30):
                print("等待%d秒后继续上传"%j)
                time.sleep(1)
        ovid=i[0]
        if int(conf("is_upload"))==1: singlePublish(ovid)

if __name__ == "__main__":
    # execute()

    # in_gen=sqlQuery("select * from in_gen")
    # sqlQuery("truncate table out_info")
    # thread_handles=[]
    # for i in in_gen: 
    #     thread_handles.append(Thread(target=singleGenerate, args=(i[0], int(i[1]),)))
    # for th in thread_handles: 
    #     th.start()
    # for th in thread_handles:
    #     th.join()

    # out_list = sqlQuery("select ovid from out_info")
    # cnt=0
    # for i in out_list:
    #     ovid=i[0]
    #     cnt+=1
    #     singlePublish(ovid)
    
    singleDownload("BV1pi4y1s763")