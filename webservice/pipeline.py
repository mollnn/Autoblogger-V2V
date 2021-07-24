from posix import times_result
import common
import spider
import os
from common import sqlQuery
import extractor
import generator
import time


def singleImport(bvid):
    print("singleImport", bvid)
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


if __name__ == "__main__":
    # clearDatafile()
    # sqlQuery("truncate table vinfo")
    # sqlQuery("truncate table danmu")
    sqlQuery("truncate table extraction")
    sqlQuery("truncate table editdesc")
    sqlQuery("truncate table status")
    
    lt=time.time()

    # singleImport("BV1q4411d7wZ")
    # singleImport("BV1sk4y1k73b")

    print("----- import",time.time()-lt)
    lt=time.time()

    singleExtract("BV1q4411d7wZ")
    
    print("----- extract",time.time()-lt)
    lt=time.time()

    singleGenerate("BV1sk4y1k73b", 1)
    
    print("----- generate",time.time()-lt)
    lt=time.time()
