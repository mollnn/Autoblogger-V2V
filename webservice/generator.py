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
# 剪辑描述符 edit_desc is a list of dict{'xvid'=?, 'start'=?, 'duration'=?}


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
    # 将剪辑描述符写入数据库
    writeEditDesc(ovid, edit_desc)
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
                clip_descs = clip_descs+clip_descs
                for i in clip_descs:
                    i["duration"] /= 2

            edit_desc += clip_descs
            last_cut_frame = frame_id

    # 选择最好的视频填入（要考虑时间限制）
    # 二分套贪心：二分一个阈值，只考虑阈值之上的片段，每个空位依次选择长度满足要求且使用次数最少的分数最高的片段
    # 限制条件：每个片段的使用次数不能超过 3

    def fillClips(score_thres):
        # 获取素材库
        srcs = sqlQuery("select id, fe-fb as len, smv from extraction where tag=%d and smv>=%f order by rand();" %
                        (tag, score_thres), isDict=True)

        edit_desc_tmp = edit_desc
        for i in srcs:
            i["cnt"] = 0
        use_max = 0
        for clip_desc in edit_desc_tmp:
            cand_id = 0
            for src_id in range(len(srcs)):
                src = srcs[src_id]
                if src["len"] <= clip_desc["duration"]*24:
                    continue
                if src["cnt"] < srcs[cand_id]["cnt"]:
                    cand_id = src_id
                elif src["smv"] > srcs[cand_id]["smv"]:
                    cand_id = src_id
            clip_desc["xvid"] = srcs[cand_id]["id"]
            srcs[cand_id]["cnt"] += 1
            use_max = max(use_max, srcs[cand_id]["cnt"])

        return edit_desc_tmp, use_max

    l = 0
    r = src_maxsmv

    while r-l > 1e-4:
        mid = (l+r)/2
        edit_desc_ans, use_max = fillClips(mid)
        if use_max > 3:
            r = mid
        else:
            l = mid

    edit_desc, use_max = fillClips(mid)
    if use_max > 3:
        print("    gen Warning: use max exceeded.")

    print(edit_desc)

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

    # 将剪辑描述符写入数据库
    writeEditDesc(ovid, edit_desc)

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
        host=MYSQL_HOST,  # 映射地址local_bind_address IP
        port=MYSQL_PORT,  # 映射地址local_bind_address端口
        user=MYSQL_USER,
        passwd=MYSQL_PASSWD,
        database=MYSQL_DBNAME,  # 需要连接的实例名
        charset='utf8')

    cursor = conn.cursor()

    datas = []

    id = 0
    for i in edit_desc:
        datas.append({"ovid": ovid, "id": id,
                     "xvid": i["xvid"], "tb": i["start"], "tt": i["duration"]})
        id += 1

    if len(datas) == 0:
        return
    keys = ', '.join(datas[0].keys())
    values = ', '.join(['%s'] * len(datas[0]))
    sql = ('insert ignore into %s (%s) values (%s);' %
           ('editdesc', keys, values))
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
