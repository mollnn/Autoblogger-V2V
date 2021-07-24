import common
import spider
import os
from common import sqlQuery
import extractor

def singleImport(bvid):
    print("singleImport",bvid)
    print("  downloadMedia",bvid)
    spider.downloadMedia(bvid)
    print("  downloadInfo",bvid)
    spider.downloadInfo(bvid)

def singleExtract(bvid):
    print("singleExtract",bvid)
    extractor.main(bvid)

def singleCompose(description, tag):
    print("singleCompose",description,tag)
    

def singlePublish(ovid):
    print("singlePublish",ovid)

def clearDatafile():
    os.system("rm ../data/media/*.mp4 -rf")
    os.system("rm ../data/edited/*.mp4 -rf")
    os.system("rm ../data/output/*.mp4 -rf")
    os.system("rm ../data/poster/*.jpg -rf")

if __name__ == "__main__":
    clearDatafile()
    # sqlQuery("truncate table vinfo")
    # sqlQuery("truncate table danmu")
    sqlQuery("truncate table extraction")
    singleImport("BV1q4411d7wZ")
    singleExtract("BV1q4411d7wZ")