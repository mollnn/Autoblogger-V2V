from posix import times_result
import common
import spider
import os
from common import sqlQuery
import extractor
import generator
import time
from threading import Thread

# 下载一个视频
def singleDownload(bvid):
    print("singleDownload", bvid)
    spider.downloadInfo(bvid)
    spider.downloadMedia(bvid)

# 导入一个视频
def singleImport(bvid):
    print("singleImport",bvid)
    spider.downloadInfo(bvid)   # 下载 vinfo+danmu 不怎么吃资源就现场下载好了
    spider.importMedia(bvid)

def singleExtract(bvid):
    print("singleExtract", bvid)
    extractor.main(bvid)


def singleGenerate(description, tag):
    print("singleGenerate", description, tag)
    generator.main(description, tag)


def singlePublish(ovid):
    print("singlePublish", ovid)


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
    for i in in_src:
        if i[0] not in download_list: download_list.append(i[0])
    for i in in_gen: 
        if len(i[0])>2 and i[0][0:2]=="BV" and i[0] not in download_list: download_list.append(i[0])

    thread_handles=[]
    for i in download_list:
        thread_handles.append(Thread(target=singleDownload, args=(i,)))
    for th in thread_handles: 
        th.start()
        time.sleep(0.5)  # 防止请求并发度过大
    for th in thread_handles:
        th.join()

    print("----- import",time.time()-lt)
    lt=time.time()

    thread_handles=[]
    for i in in_src: 
        thread_handles.append(Thread(target=singleExtract, args=(i[0],)))
    for th in thread_handles: 
        th.start()
    for th in thread_handles:
        th.join()
    
    print("----- extract",time.time()-lt)
    lt=time.time()

    thread_handles=[]
    for i in in_gen: 
        thread_handles.append(Thread(target=singleGenerate, args=(i[0], int(i[1]),)))
    for th in thread_handles: 
        th.start()
    for th in thread_handles:
        th.join()

    print("----- generate",time.time()-lt)

if __name__ == "__main__":
    execute()
    # sqlQuery("truncate table edition")
    # sqlQuery("truncate table status")
    # sqlQuery("truncate table out_info")
    # in_gen=sqlQuery("select * from in_gen")
    # thread_handles=[]
    # for i in in_gen: 
    #     thread_handles.append(Thread(target=singleGenerate, args=(i[0], int(i[1]),)))
    # for th in thread_handles: 
    #     th.start()
    # for th in thread_handles:
    #     th.join()