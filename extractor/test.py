import threading
import os
import common
import spider
import shotcut
import cutter_danmu

def fuck(bvid):
    print("THREAD START ",bvid)
    filename = "/home/wzc/mtmp/%s.mp4" % bvid
    if os.path.isfile(("/home/wzc/mtmp/%s.mp4" % bvid)) == False:
        print("INVALID INPUT FILE.")
        return

    spider.importMedia(bvid,filename)
    spider.downloadInfo(bvid)
    shotcut.shotcut(bvid)
    cutter_danmu.solve(bvid)


sql_res = common.query("banime", "select distinct bvid from Vinfo")
for i in sql_res:
    fuck(i[0])
