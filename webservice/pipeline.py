from posix import times_result
import common
import spider
import os
from common import sqlQuery
import extractor
import generator
import time
from threading import Thread

def singleDownload(bvid):
    print("singleDownload", bvid)
    spider.downloadInfo(bvid)
    spider.downloadMedia(bvid)


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
    sqlQuery("truncate table editdesc")
    sqlQuery("truncate table status")
    
    in_src=sqlQuery("select * from in_src")
    in_gen=sqlQuery("select * from in_gen")

    lt=time.time()

    download_list=[]
    for i in in_src: download_list.append(i[0])
    for i in in_gen: 
        if len(i[0])>2 and i[0][0:2]=="BV": download_list.append(i[0])

    thread_handles=[]
    for i in download_list:
        thread_handles.append(Thread(target=singleDownload, args=(i,)))
    for th in thread_handles: 
        th.start()
        time.sleep(0.2)  # 防止请求并发度过大
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

    for i in in_gen: 
        singleGenerate(i[0], int(i[1]))
    
    print("----- generate",time.time()-lt)

if __name__ == "__main__":
    execute()