import sys
sys.path.append("..")
import threading
import database.msql
import os
import extractor.pipeline


def Fuck(bvid):
    print("THREAD START ",bvid)
    filename = "/home/wzc/mtmp/%s.mp4" % bvid
    if os.path.isfile(("/home/wzc/mtmp/%s.mp4" % bvid)) == False:
        print("INVALID INPUT FILE.")
        return
    extractor.pipeline.importMedia(bvid, filename)
    extractor.pipeline.downloadInfo(bvid)
    extractor.pipeline.shotCut(bvid)
    extractor.pipeline.extract(bvid, 0, 0)
    extractor.pipeline.extract(bvid, 0, 1)
    extractor.pipeline.extract(bvid, 0, 2)
    extractor.pipeline.extract(bvid, 0, 3)


def ExecuteThreads(thread_handles):
    for i in thread_handles:
        i.start()
    for i in thread_handles:
        i.join()
    print("test.icopy: Batch End")


sql_res = database.msql.query("banime", "select distinct bvid from Vinfo")

thread_handles = []

for i in sql_res:
    bvid = i[0]
    thread_handle = threading.Thread(target=Fuck, args=(bvid,))
    thread_handles.append(thread_handle)
    if len(thread_handles) >= 64:
        ExecuteThreads(thread_handles)
        thread_handles = []
ExecuteThreads(thread_handles)

print("test.icopy: All End")
