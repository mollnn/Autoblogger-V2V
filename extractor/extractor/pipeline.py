import sys
sys.path.append("..")

import algorithm.shotcut.shotcut
import database.msql
import control.cutidgen
import spider.stable
import extractor.naive
import sys
import download.biliMedia
import os.path

# --- Function List ---
# def downloadMedia(bvid):
# def downloadInfo(bvid):
# def shotCut(bvid):
# def extract(bvid, src_type, clip_type):
# ---------------------

def extract(bvid, src_type, clip_type):
    if len(database.msql.query("biliextract", """
        select * from extraction where bvid='{bvid}' and src_type='{src_type}' and clip_type='{clip_type}'
        """.format(bvid=bvid, src_type=src_type, clip_type=clip_type))) > 0:
        print("extractor.main.extract: Already extracted with same bvid, src_type and clip_type. Terminated.")
        return
    if src_type == 0 and clip_type == 0:
        extractor.naive.solve(bvid)
    else:
        print("Unsupported Type Parameters!")


def shotCut(bvid):
    if len(database.msql.query("biliextract", """
        select * from shotcut where bvid='{bvid}'
        """.format(bvid=bvid))) > 0:
        print("extractor.main.doShotCut: Already cut. Shotcut process terminated.")
        return

    ans = algorithm.shotcut.shotcut.shotcut('../../data/media/'+bvid+'.mp4')

    for item in ans:
        cutid = control.cutidgen.generateId()
        if item["transition"] == "gradual":
            database.msql.query("biliextract", """
                insert into shotcut 
                (bvid, cutid, transition, start_frame, end_frame)
                values
                ('%s','%s','%s','%d','%d')
                """ % (bvid, cutid, item["transition"], item["start_frame"], item["end_frame"]))
        else:
            database.msql.query("biliextract", """
                insert into shotcut 
                (bvid, cutid, transition, cut_frame)
                values
                ('%s','%s','%s','%d')
                """ % (bvid, cutid, item["transition"], item["cut_frame"]))

    print("extractor.main.doShotCut: Finish all SQL Writing.")


def downloadInfo(bvid):
    ans = database.msql.query(
        "biliextract", "select * from Vinfo where bvid='%s'" % bvid)
    if len(ans) > 0:
        print("extractor.main.downloadInfo: Info already exists. Terminated.")
        return
    spider.stable.solve(bvid)


def downloadMedia(bvid):
    if os.path.isfile('../../data/media/'+bvid+'.mp4'):
        print("extractor.main.downloadMedia: Media already exists. Terminated.")
    download.biliMedia.getMP4ByBid(
        bvid, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")
