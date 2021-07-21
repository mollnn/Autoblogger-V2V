import sys
sys.path.append("..")
import algorithm.shotcut.shotcut
import cv2driver
import cv2
from matplotlib import pyplot as plt
import ffmpeg
import json
import os.path
import os
import download.biliMedia
import extractor.naive
import extractor.xlove
import extractor.xshock
import extractor.xhumor
import spider.stable
import control.jsonconfig
import control.cutidgen
import database.msql
import media.importer
import media.editor


def downloadMedia(bvid):
    print("edimitator.edimitator.downloadMedia: Hello!")
    if os.path.isfile('../../data/media/'+bvid+'.mp4'):
        print("edimitator.edimitator.downloadMedia: Media already exists. Terminated.")
        return
    download.biliMedia.getMP4ByBid(
        bvid, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")


def shotCut(bvid):
    return algorithm.shotcut.shotcut.shotcut("../../data/media/%s.mp4" % bvid)


def calcShotcutFlag(shotcut_list, n_frame):
    shotcut_flags = [0]*n_frame
    for shotcut in shotcut_list:
        if shotcut["transition"] == "cut":
            shotcut_flags[shotcut["cut_frame"]] = 1
        else:
            shotcut_flags[shotcut["start_frame"]] = 2
            shotcut_flags[shotcut["end_frame"]] = 3
    return shotcut_flags


def edimitator(bvid):
    downloadMedia(bvid)
    video_filename = "../../data/media/%s.mp4" % bvid
    video = cv2driver.readVideo(video_filename)
    n_frame = len(video)
    shotcut_list = shotCut(bvid)
    shotcut_flags = calcShotcutFlag(shotcut_list, n_frame)
    output_video_filename = "output.avi"
    edit_desc=[]
    last_cut_frame=0
    for i in range(n_frame):
        try:
            frame = video[i]
            if shotcut_flags[i] >0:
                clip_begin=last_cut_frame
                clip_end=i
                clip_duration=i-last_cut_frame
                clip_desc={"filename":"","start":0,"duration":clip_duration/24}
                edit_desc.append(clip_desc)
                last_cut_frame=i
        except Exception:
            print("error")
    for i in edit_desc:
        ans=database.msql.query(control.jsonconfig.readConfig("dbname"), "select id from extraction where clip_type=1 and frame_end-frame_begin>%d order by rand() limit 1;"%int(i["duration"]*24))
        i["filename"]="../../data/output/%s.mp4"%ans[0][0]
        print(i)
    media.editor.edit(edit_desc,"output_mid.mp4")
    os.system("ffmpeg -i output_mid.mp4 -i %s -c copy -map 0:0 -map 1:1 -y -shortest output.mp4" % video_filename)

if __name__ == "__main__":
    edimitator("BV1cE41147vF")
