import threading
import os
import pipeline
import common

def Fuck(bvid):
    print("THREAD START ",bvid)
    filename = "/home/wzc/mtmp/%s.mp4" % bvid
    if os.path.isfile(("/home/wzc/mtmp/%s.mp4" % bvid)) == False:
        print("INVALID INPUT FILE.")
        return
    pipeline.importMedia(bvid, filename)
    pipeline.downloadInfo(bvid)
    pipeline.shotCut(bvid)
    pipeline.extract(bvid, 0, 0)
    pipeline.extract(bvid, 0, 1)
    pipeline.extract(bvid, 0, 2)
    pipeline.extract(bvid, 0, 3)


def ExecuteThreads(thread_handles):
    for i in thread_handles:
        i.start()
    for i in thread_handles:
        i.join()
    print("test.icopy: Batch End")

sql_res = common.query("banime", "select distinct bvid from Vinfo")
thread_handles = []

for i in sql_res:
    bvid = i[0]
    thread_handle = threading.Thread(target=Fuck, args=(bvid,))
    thread_handles.append(thread_handle)
    if len(thread_handles) >= 1:
        ExecuteThreads(thread_handles)
        thread_handles = []
ExecuteThreads(thread_handles)

print("test.icopy: All End")
