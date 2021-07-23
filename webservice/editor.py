from threading import Thread
import ffmpeg
import json
import os
import re
import json
import common

# 根据片段描述符数组剪辑视频
# clip_desc_list is a list of dict{'filename'=?, 'start'=?, 'duration'=?}
def edit(clip_desc_list, output_filename, quiet=True):
    clip_list = []
    ffcmd="""ffmpeg -i "concat:"""
    flag=0
    def _solve_one(clip_desc):
        os.system("ffmpeg -i %s -ss %f -t %f -b:v 1000k ../tmp/%s.ts %s"%(clip_desc["filename"],clip_desc["start"],clip_desc["duration"],clip_desc["tid"],common.readConfig("ffmpeg_quiet")+common.readConfig("ffmpeg_default")))
    handles=[]
    for clip_desc in clip_desc_list:
        if 'xvid' in clip_desc:
            clip_desc["filename"]="../data/output/%s.hd.mp4"%clip_desc["xvid"] if clip_desc["xvid"]!="" else "../data/media/black.hd.avi"
        clip_desc["tid"]=common.generateTempid()
        th=Thread(target=_solve_one,args=(clip_desc,))
        th.start()
        handles.append(th)
        ffcmd+=("|" if flag==1 else "") + "../tmp/%s.ts"%clip_desc["tid"]
        flag=1
    for i in handles:
        i.join()
    ffcmd+="""" -vcodec libx264 -acodec aac -b:v 100k %s"""%output_filename
    ffcmd+=" "+common.readConfig("ffmpeg_default")+common.readConfig("ffmpeg_quiet")
    os.system(ffcmd)

def edit_by_ovid(ovid):
    edit_desc = common.query(common.readConfig("dbname"), "select * from out_editdesc where ovid='%s';"%ovid, isDict=True)
    output_filename="../data/edited/%s.mp4"%ovid
    edit(edit_desc,output_filename+".temp.mp4")
    template_bvid=common.query(common.readConfig("dbname"), "select bvid from out_template where ovid='%s'"%ovid)[0][0]
    os.system("ffmpeg -i "+output_filename+".temp.mp4"+" -i ../data/media/%s.hd.mp4 -c copy -map 0:0 -map 1:1 -y %s %s" % (template_bvid,output_filename,common.readConfig("ffmpeg_quiet")))
    common.query(common.readConfig("dbname"), "insert ignore into state_out (ovid,`desc`) values ('%s','%s')" % (ovid,"ok"))
