import common
from common import sqlQuery
from common import conf
from shotcut import shotcut
import ffmpeg
import math
import numpy as np
import os


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
    l = np.min(score)
    r = np.max(score)
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
    for clip in clips:
        xvid = common.generateXvid()
        l, r = clip[0], clip[1]
        score_argmax = np.argmax(score[l:r])+l
        score_max = np.max(score[l:r])
        os.system("ffmpeg -i {fin} -ss {ts} -t {tt} {fout} {fg}".format(fg=conf("ffmpeg_default"),
                  fin="../data/media/%s.mp4" % bvid, fout="../data/output/%s.mp4" % xvid, ts=l/frame_rate, tt=(r-l)/frame_rate))
        os.system("ffmpeg -i {fin} -ss {ts} -t {tt} {fout} {fg}".format(fg=conf("ffmpeg_default"),
                  fin="../data/media/%s.hd.mp4" % bvid, fout="../data/output/%s.hd.mp4" % xvid, ts=l/frame_rate, tt=(r-l)/frame_rate))
        os.system("ffmpeg -i {fin} -ss 00:00:00 -vframes 1 {fout} {fg}".format(fg=conf(
            "ffmpeg_default"), fin="../data/output/%s.mp4" % xvid, fout="../data/poster/%s.jpg" % xvid))
        sqlQuery("insert into extraction (id,bvid,tag,fb,fe,smv,smp) values ('%s','%s',%d,%d,%d,%d,%d)" % (
            xvid, bvid, tag, l, r, score_max, score_argmax))

    print("  extractor.sine: ok")


def main(bvid):
    print("  extractor: shotcut...")
    shotcuts = shotcut(bvid)

    print("  extractor: read danmu...")
    cid = sqlQuery(
        "select cid from vinfo where bvid='{bvid}'".format(bvid=bvid))[0][0]
    danmus = sqlQuery(
        "select * from danmu where cid='{cid}'".format(cid=cid), isDict=True)

    # 在这里接入您的 extractor
    extractor_sine(0, bvid, danmus, shotcuts)
