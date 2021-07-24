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
    spider.downloadMedia(bvid)
    spider.downloadInfo(bvid)


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
    
    lt=time.time()

    # singleImport("BV1q4411d7wZ")

    print("--- import",time.time()-lt)
    lt=time.time()

    singleExtract("BV1q4411d7wZ")
    
    print("--- extract",time.time()-lt)
    lt=time.time()

    singleGenerate("ConcatAll", 0)
    
    print("--- generate",time.time()-lt)
    lt=time.time()
