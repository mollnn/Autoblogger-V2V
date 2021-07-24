import common
from common import sqlQuery
from common import conf
from shotcut import shotcut
import ffmpeg
import math
import numpy as np
import os
from threading import Thread
import random

def export_clips(clips, score, bvid, frame_rate, tag):
    # 片段输出封装
    thread_handles=[]
    for clip in clips:
        def A():
            xvid = common.generateXvid()
            l, r = clip[0], clip[1]
            score_argmax = np.argmax(score[l:r])+l
            score_max = np.max(score[l:r])
            os.system("ffmpeg -i {fin} -ss {ts} -t {tt} {cfg} {fout} {fg}".format(
                fg=conf("ffmpeg_default"),
                fin="../data/media/%s.mp4" % bvid,
                fout="../data/output/%s.mp4" % xvid,
                ts=l/frame_rate,
                tt=(r-l)/frame_rate,
                cfg=conf("ffmpeg_ld")
            ))
            os.system("ffmpeg -i {fin} -ss {ts} -t {tt} {cfg} {fout} {fg}".format(
                fg=conf("ffmpeg_default"),
                fin="../data/media/%s.hd.mp4" % bvid,
                fout="../data/output/%s.hd.mp4" % xvid,
                ts=l/frame_rate,
                tt=(r-l)/frame_rate,
                cfg=conf("ffmpeg_hd")
            ))
            os.system("ffmpeg -i {fin} -ss 00:00:00 -vframes 1 {fout} {fg}".format(
                fg=conf("ffmpeg_default"),
                fin="../data/output/%s.mp4" % xvid,
                fout="../data/poster/%s.jpg" % xvid
            ))
            sqlQuery("insert into extraction (id,bvid,tag,fb,fe,smv,smp) values ('%s','%s',%d,%d,%d,%d,%d)"
                    % (xvid, bvid, tag, l, r, score_max, score_argmax))
        thread_handles.append(Thread(target=A))
    for th in thread_handles: th.start()
    for th in thread_handles: th.join()
    

def extractor_sine(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    # 读取基本信息
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     bvid)["format"]["duration"])
    frame_rate = 24
    n_frame = int(math.ceil(duration*frame_rate))

    # 计算评分（! 自行修改）
    score = [1+math.sin(i/1e3) for i in range(n_frame)]

    # 转场处评分归零
    for cut in shotcuts:
        cut_begin = cut["cut_frame"] if cut["transition"] == "cut" else cut["start_frame"]
        cut_end = cut["cut_frame"] if cut["transition"] == "cut" else cut["end_frame"]
        for i in range(cut_begin, cut_end+1):
            if 0 <= i and i < n_frame:
                score[i] = 0

    # 控制时长要求与提取比例（! 自行修改）
    ratio = 0.2
    len_min = 3*24
    len_max = 20*24

    # 二分确定阈值
    l = np.min(score)+1e-5
    r = np.max(score)-1e-5
    while r-l > 1e-4:
        mid = (l+r)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            l = mid
        else:
            r = mid

    # 区间列表生成
    threshold = l
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.sine:", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)

    print("  extractor.sine: ok")


def main(bvid):
    print("  extractor: prep...")

    common.wstat(bvid, 0+random.randint(0,5), ext=True)

    shotcuts = shotcut(bvid)

    common.wstat(bvid, 30+random.randint(0,10), ext=True)

    cid = sqlQuery(
        "select cid from vinfo where bvid='{bvid}'".format(bvid=bvid))[0][0]
    danmus = sqlQuery(
        "select * from danmu where cid='{cid}'".format(cid=cid), isDict=True)

    common.wstat(bvid, 40+random.randint(0,20), ext=True)

    # 在这里接入您的 extractor
    extractor_sine(0, bvid, danmus, shotcuts)

    common.wstat(bvid, 100, ext=True)