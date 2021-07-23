import os
import common
import editor
import shotcut

def calcShotcutFlag(shotcut_list, n_frame):
    shotcut_flags = [0]*n_frame
    for shotcut in shotcut_list:
        if shotcut["transition"] == "cut":
            shotcut_flags[min(n_frame-1, shotcut["cut_frame"])] = 1
        else:
            shotcut_flags[min(n_frame-1,shotcut["start_frame"])] = 2
            shotcut_flags[min(n_frame-1,shotcut["end_frame"])] = 3
    return shotcut_flags


def generate(bvid, src_type, clip_type):
    ovid=common.generateOvid()
    video_filename = "../data/media/%s.mp4" % bvid
    video = common.readVideo(video_filename)
    n_frame = len(video)
    shotcut_list = shotcut.shotcut(bvid)
    shotcut_flags = calcShotcutFlag(shotcut_list, n_frame)
    edit_desc=[]
    last_cut_frame=0
    for i in range(n_frame):
        try:
            frame = video[i]
            if shotcut_flags[i] >0:
                clip_begin=last_cut_frame
                clip_end=i
                clip_duration=i-last_cut_frame
                clip_desc={"xvid":"","start":0,"duration":clip_duration/24}
                edit_desc.append(clip_desc)
                last_cut_frame=i
        except Exception:
            print("error")
    for i in edit_desc:
        ans=common.query(common.readConfig("dbname"), "select id from extraction where src_type=%d and clip_type=%d and frame_end-frame_begin>%d order by rand() limit 1;"%(src_type, clip_type, int(i["duration"]*24)))
        if len(ans)>0:
            i["xvid"]=ans[0][0]
    id=0
    for i in edit_desc:
        common.query(common.readConfig("dbname"), "insert ignore into out_editdesc (ovid, id, xvid, start, duration) values ('%s',%d,'%s',%f,%f)"%(ovid, id, i["xvid"], i["start"],i["duration"]))
        id+=1
    common.query(common.readConfig("dbname"), "insert ignore into out_template (ovid, bvid) values ('%s','%s')"%(ovid, bvid))
    return ovid
    # editor.edit(edit_desc,"output_mid.mp4")
    # os.system("ffmpeg -i output_mid.mp4 -i %s -c copy -map 0:0 -map 1:1 -y -shortest output.mp4" % video_filename)
