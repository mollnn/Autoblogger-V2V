from random import randint
import common
import os
import ffmpeg
from common import conf
from common import sqlQuery
from threading import Thread
import random
import math
import shotcut
import pymysql
import json

# 剪辑描述符 edit_desc is a list of dict{'xvid'=?, 'start'=?, 'duration'=?}


############################################################################
# 在这里编写您的生成器

def generateByConcatAll(description, tag):
    # 此函数返回一个剪辑描述符
    # 自行从数据表 extraction 中读取素材
    ovid = common.generateOvid()
    common.wstat(ovid, random.randint(0, 5))
    src_clips = sqlQuery(
        "select id, fe-fb as len from extraction where tag=%d" % tag)

    edit_desc = [{"xvid": src_clip[0], "start":0,
                  "duration":src_clip[1]/24} for src_clip in src_clips]
    # 根据剪辑描述符剪辑视频
    edit(edit_desc, "../data/edited/%s.mp4" % ovid)
    # 生成视频封面
    os.system("ffmpeg -i {fin} -ss 00:00:00 -vframes 1 {fout} {fg}".format(
        fg=conf("ffmpeg_default"),
        fin="../data/edited/%s.mp4" % ovid,
        fout="../data/poster/%s.jpg" % ovid
    ))
    # 将剪辑描述符写入数据库
    writeEditDesc(ovid, edit_desc)
    # 将 OV 信息写入数据库
    sqlQuery("insert into out_info (ovid, description, tag) values ('%s','%s',%d)"%(ovid, description, tag))
    common.wstat(ovid, 100)


def generateByVideoTemplate(template_bvid, tag):
    # 此函数返回一个剪辑描述符
    # 自行从数据表 extraction 中读取素材
    ovid = common.generateOvid()
    common.wstat(ovid, random.randint(0, 5))
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     template_bvid)["format"]["duration"])
    frame_rate = 24     # Forced
    n_frame = int(math.ceil(duration*frame_rate))

    # 分析模板视频中的转场情况
    shotcut_list = shotcut.shotcut(template_bvid)
    shotcut_tag = [0]*n_frame
    for shot_cut in shotcut_list:
        if shot_cut["transition"] == "cut":
            shotcut_tag[min(n_frame-1, shot_cut["cut_frame"])] = 1
        else:
            shotcut_tag[min(n_frame-1, shot_cut["start_frame"])] = 2
            shotcut_tag[min(n_frame-1, shot_cut["end_frame"])] = 3

    # 获取素材库中素材的最大长度
    src_maxlen = int(sqlQuery(
        "select fe-fb as len from extraction where tag=%d order by len desc limit 1;" % tag)[0][0])
    src_maxsmv = float(
        sqlQuery("select max(smv) from extraction where tag=%d;" % tag)[0][0])

    # 生成剪辑描述（视频文件待定）
    edit_desc = []
    last_cut_frame = 0
    for frame_id in range(n_frame):
        if shotcut_tag[frame_id] > 0:
            clip_duration = frame_id-last_cut_frame
            clip_desc = {"xvid": "", "start": 0, "duration": clip_duration/24}

            # 处理空位超出素材库最大长度的情况（递归等分下去，直到满足）
            clip_descs = [clip_desc]
            while clip_descs[0]["duration"]*24 >= src_maxlen:
                print("    gen Warning: slot too long, reduced.")
                clip_descs += [i.copy() for i in clip_descs]
                for i in clip_descs:
                    i["duration"] /= 2

            edit_desc += clip_descs[:]
            last_cut_frame = frame_id

    for i in range(len(edit_desc)):
        edit_desc[i]["id"]=i

    # 选择最好的视频填入（要考虑时间限制）
    # 二分套随机化：二分一个阈值，只考虑阈值之上的片段，每个空位随机选择一个长度符合要求的片段
    # 限制条件：片段尽量减少重复使用

    def fillClips(score_thres):
        print("bisect testing... ",score_thres)
        # 获取素材库
        src_lib = sqlQuery("select id, fe-fb as len, smv from extraction where tag=%d and smv>=%f order by rand();" %
                        (tag, score_thres), isDict=True)
        print(json.dumps(src_lib).replace("{","\n{"))
        edit_desc_tmp = edit_desc[:]
        for i in src_lib:
            i["cnt"] = 0
        clip_max_usage = 0
        last_use = -1
        for i in range(len(edit_desc_tmp)):
            candidate_id = random.randint(0,len(src_lib)-1)
            lim = 1000
            while src_lib[candidate_id]["len"] <= edit_desc_tmp[i]["duration"]*24 or candidate_id==last_use:
                candidate_id = random.randint(0,len(src_lib)-1)
                lim-=1
                if lim==0: 
                    print("fail")
                    return edit_desc_tmp, 1e9
            print("choose ",i,candidate_id)
            edit_desc_tmp[i]["xvid"] = src_lib[candidate_id]["id"]
            last_use=candidate_id
            src_lib[candidate_id]["cnt"] += 1
            clip_max_usage = max(clip_max_usage, src_lib[candidate_id]["cnt"])
        print(json.dumps(edit_desc_tmp).replace("{","\n{"))
        return edit_desc_tmp, clip_max_usage

    bisect_l = 0
    bisect_r = src_maxsmv-1e-4

    while bisect_r-bisect_l > 1e-3:
        bisect_mid = (bisect_l+bisect_r)/2
        edit_desc_ans, clip_max_usage = fillClips(bisect_mid)
        if clip_max_usage > 3:
            bisect_r = bisect_mid
        else:
            bisect_l = bisect_mid

    print("bisect_mid", bisect_mid)

    edit_desc, clip_max_usage = fillClips(bisect_mid)
    if clip_max_usage > 3:
        print("    gen Warning: use max exceeded.")

    # 根据剪辑描述符剪辑视频
    edit(edit_desc, "../tmp/%s.vtmp.mp4" % ovid)

    # 特殊：替换音轨
    os.system("ffmpeg -i {fin_v} -i {fin_a} {cfg} {fout} {fg}".format(
        fin_v="../tmp/%s.vtmp.mp4" % ovid,
        fin_a="../data/media/%s.hd.mp4" % template_bvid,
        cfg="-c copy -map 0:0 -map 1:1 -y",
        fout="../data/edited/%s.mp4" % ovid,
        fg=conf("ffmpeg_default")
    ))

    # 生成视频封面
    os.system("ffmpeg -i {fin} -ss 00:00:00 -vframes 1 {fout} {fg}".format(
        fg=conf("ffmpeg_default"),
        fin="../data/edited/%s.mp4" % ovid,
        fout="../data/poster/%s.jpg" % ovid
    ))

    # 将剪辑描述符写入数据库
    writeEditDesc(ovid, edit_desc)
    # 将 OV 信息写入数据库
    sqlQuery("insert into out_info (ovid, description, tag) values ('%s','%s',%d)"%(ovid, template_bvid, tag))
    common.wstat(ovid, 100)

###########################################################################


def edit(edit_desc, output_filename):
    # 根据剪辑描述符剪辑视频
    # 先把每个片段切成 .ts
    ts_list = []
    thread_handles = []
    for i in edit_desc:
        def A(clip_desc):
            tsid = common.generateTempid()
            ts_list.append(tsid)
            os.system("ffmpeg -i {fin} -ss {ts} -t {tt} -b:v 20000k {fout} {fg}".format(
                fin="../data/output/%s.hd.mp4" % clip_desc["xvid"],
                ts=clip_desc["start"],
                tt=clip_desc["duration"],
                fout="../tmp/%s.ts" % tsid,
                fg=conf("ffmpeg_default")
            ))
        thread_handles.append(Thread(target=A, args=(i,)))
    for th in thread_handles:
        th.start()
    for th in thread_handles:
        th.join()

    # 将一堆 .ts 合并并重新编码
    os.system(""" ffmpeg -i "concat:{fin}" {fconf} {fout} {fg}""".format(
        fin="|".join(["../tmp/%s.ts" % tsid for tsid in ts_list]),
        fconf="-vcodec libx264 -acodec aac -b:v 300k",
        fout=output_filename,
        fg=conf("ffmpeg_default")
    ))

def writeEditDesc(ovid, edit_desc):
    MYSQL_DBNAME = common.readConfig("dbname")
    MYSQL_HOST = common.readConfig("mysql_host")
    MYSQL_USER = common.readConfig("mysql_user")
    MYSQL_PASSWD = common.readConfig("mysql_password")
    MYSQL_PORT = common.readConfig("mysql_port")

    conn = pymysql.connect(
        host=MYSQL_HOST, 
        port=MYSQL_PORT,
        user=MYSQL_USER,
        passwd=MYSQL_PASSWD,
        database=MYSQL_DBNAME, 
        charset='utf8')

    cursor = conn.cursor()

    datas = []

    for i in edit_desc:
        datas.append({"ovid": ovid, "id": i["id"],
                     "xvid": i["xvid"], "tb": i["start"], "tt": i["duration"]})

    if len(datas) == 0:
        return
    keys = ', '.join(datas[0].keys())
    values = ', '.join(['%s'] * len(datas[0]))
    sql = ('insert ignore into %s (%s) values (%s);' %
           ('edition', keys, values))
    ls = []
    for data in datas:
        ls.append(tuple(data.values()))
    cursor.executemany(sql, ls)
    conn.commit()

    cursor.close()
    conn.close()


def main(description, tag):
    # description: 生成方法描述
    # tag: 素材标记号
    # 按照 description 的方法（可能是视频模板，可能是音乐），利用所有带 tag 的素材生成视频

    if description == "ConcatAll":
        edit_desc = generateByConcatAll(description, tag)
    elif len(description) > 2 and description[0:2] == "BV":
        # 按视频模板剪辑
        edit_desc = generateByVideoTemplate(description, tag)
