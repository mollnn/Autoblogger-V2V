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
import scipy.signal

def export_clips(clips, score, bvid, frame_rate, tag):
    # 片段输出封装
    thread_handles=[]
    for i in clips:
        def A(clip):
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
            sqlQuery("insert into extraction (id,bvid,tag,fb,fe,smv,smp) values ('%s','%s',%d,%d,%d,%f,%d)"
                    % (xvid, bvid, tag, l, r, score_max, score_argmax))
        thread_handles.append(Thread(target=A,args=(i,)))
    for th in thread_handles: th.start()
    for th in thread_handles: th.join()


########################################################################
# 提取器们


#####################################################
# 0 号提取器


def extractor_sine(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    return # 这个提取器实际上荒废，仅供作为编写提取器的参考，以及特殊测试时使用

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
    ratio = 0.1
    len_min = 3*24
    len_max = 20*24

    # 二分确定阈值
    bisect_left = np.min(score)+1e-5
    bisect_right = np.max(score)-1e-5
    while bisect_right-bisect_left > 1e-4:
        mid = (bisect_left+bisect_right)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            bisect_left = mid
        else:
            bisect_right = mid

    # 区间列表生成
    threshold = bisect_left
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.sine: report: ", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)



#####################################################
# 1 号提取器


def extractor_danmu_density(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    # 读取基本信息
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     bvid)["format"]["duration"])
    frame_rate = 24
    n_frame = int(math.ceil(duration*frame_rate))

    # 计算评分（! 自行修改）
    score = [0]*n_frame
    for danmu in danmus: score[max(0, min(n_frame-1, int(float(danmu["floattime"]*24))))]+=1
    score=scipy.signal.savgol_filter(score,49,3)  
    score=[max(i,0) for i in score]

    # 转场处评分归零
    for cut in shotcuts:
        cut_begin = cut["cut_frame"] if cut["transition"] == "cut" else cut["start_frame"]
        cut_end = cut["cut_frame"] if cut["transition"] == "cut" else cut["end_frame"]
        for i in range(cut_begin, cut_end+1):
            if 0 <= i and i < n_frame:
                score[i] = 0

    # 控制时长要求与提取比例（! 自行修改）
    ratio = 0.2
    len_min = 2*24
    len_max = 20*24

    # 二分确定阈值
    bisect_left = np.min(score)+1e-5
    bisect_right = np.max(score)-1e-5
    while bisect_right-bisect_left > 1e-4:
        mid = (bisect_left+bisect_right)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            bisect_left = mid
        else:
            bisect_right = mid

    # 区间列表生成
    threshold = bisect_left
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.danmu_density: report: ", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)


#####################################################
# 2 号提取器


def extractor_hot(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    return # 要启用该提取器，请删除本行

    # 读取基本信息
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     bvid)["format"]["duration"])
    frame_rate = 24
    n_frame = int(math.ceil(duration*frame_rate))

    # 计算评分（! 自行修改）
    score = [0]*n_frame
    for danmu in danmus: score[max(0, min(n_frame-1, int(float(danmu["floattime"]*24))))]+=1
    score=scipy.signal.savgol_filter(score,49,3)  
    score=[max(i,0) for i in score]

    # 转场处评分归零
    for cut in shotcuts:
        cut_begin = cut["cut_frame"] if cut["transition"] == "cut" else cut["start_frame"]
        cut_end = cut["cut_frame"] if cut["transition"] == "cut" else cut["end_frame"]
        for i in range(cut_begin, cut_end+1):
            if 0 <= i and i < n_frame:
                score[i] = 0

    # 控制时长要求与提取比例（! 自行修改）
    ratio = 0.05
    len_min = 3*24
    len_max = 20*24

    # 二分确定阈值
    bisect_left = np.min(score)+1e-5
    bisect_right = np.max(score)-1e-5
    while bisect_right-bisect_left > 1e-4:
        mid = (bisect_left+bisect_right)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            bisect_left = mid
        else:
            bisect_right = mid

    # 区间列表生成
    threshold = bisect_left
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.danmu_density: report: ", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)


#####################################################
# 3 号提取器

def extractor_love(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    return # 要启用该提取器，请删除本行

    # 读取基本信息
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     bvid)["format"]["duration"])
    frame_rate = 24
    n_frame = int(math.ceil(duration*frame_rate))

    # 计算评分（! 自行修改）
    score = [0]*n_frame
    for danmu in danmus: score[max(0, min(n_frame-1, int(float(danmu["floattime"]*24))))]+=1
    score=scipy.signal.savgol_filter(score,49,3)  
    score=[max(i,0) for i in score]

    # 转场处评分归零
    for cut in shotcuts:
        cut_begin = cut["cut_frame"] if cut["transition"] == "cut" else cut["start_frame"]
        cut_end = cut["cut_frame"] if cut["transition"] == "cut" else cut["end_frame"]
        for i in range(cut_begin, cut_end+1):
            if 0 <= i and i < n_frame:
                score[i] = 0

    # 控制时长要求与提取比例（! 自行修改）
    ratio = 0.05
    len_min = 3*24
    len_max = 20*24

    # 二分确定阈值
    bisect_left = np.min(score)+1e-5
    bisect_right = np.max(score)-1e-5
    while bisect_right-bisect_left > 1e-4:
        mid = (bisect_left+bisect_right)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            bisect_left = mid
        else:
            bisect_right = mid

    # 区间列表生成
    threshold = bisect_left
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.danmu_density: report: ", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)


#####################################################
# 4 号提取器

def extractor_shock(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    return # 要启用该提取器，请删除本行

    # 读取基本信息
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     bvid)["format"]["duration"])
    frame_rate = 24
    n_frame = int(math.ceil(duration*frame_rate))

    # 计算评分（! 自行修改）
    score = [0]*n_frame
    for danmu in danmus: score[max(0, min(n_frame-1, int(float(danmu["floattime"]*24))))]+=1
    score=scipy.signal.savgol_filter(score,49,3)  
    score=[max(i,0) for i in score]

    # 转场处评分归零
    for cut in shotcuts:
        cut_begin = cut["cut_frame"] if cut["transition"] == "cut" else cut["start_frame"]
        cut_end = cut["cut_frame"] if cut["transition"] == "cut" else cut["end_frame"]
        for i in range(cut_begin, cut_end+1):
            if 0 <= i and i < n_frame:
                score[i] = 0

    # 控制时长要求与提取比例（! 自行修改）
    ratio = 0.05
    len_min = 3*24
    len_max = 20*24

    # 二分确定阈值
    bisect_left = np.min(score)+1e-5
    bisect_right = np.max(score)-1e-5
    while bisect_right-bisect_left > 1e-4:
        mid = (bisect_left+bisect_right)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            bisect_left = mid
        else:
            bisect_right = mid

    # 区间列表生成
    threshold = bisect_left
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.danmu_density: report: ", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)

#####################################################
# 5 号提取器

def extractor_humor(tag, bvid, danmus, shotcuts):
    # tag: 提取的素材标记

    return # 要启用该提取器，请删除本行

    # 读取基本信息
    duration = float(ffmpeg.probe("../data/media/%s.mp4" %
                     bvid)["format"]["duration"])
    frame_rate = 24
    n_frame = int(math.ceil(duration*frame_rate))

    # 计算评分（! 自行修改）
    score = [0]*n_frame
    for danmu in danmus: score[max(0, min(n_frame-1, int(float(danmu["floattime"]*24))))]+=1
    score=scipy.signal.savgol_filter(score,49,3)  
    score=[max(i,0) for i in score]

    # 转场处评分归零
    for cut in shotcuts:
        cut_begin = cut["cut_frame"] if cut["transition"] == "cut" else cut["start_frame"]
        cut_end = cut["cut_frame"] if cut["transition"] == "cut" else cut["end_frame"]
        for i in range(cut_begin, cut_end+1):
            if 0 <= i and i < n_frame:
                score[i] = 0

    # 控制时长要求与提取比例（! 自行修改）
    ratio = 0.05
    len_min = 3*24
    len_max = 20*24

    # 二分确定阈值
    bisect_left = np.min(score)+1e-5
    bisect_right = np.max(score)-1e-5
    while bisect_right-bisect_left > 1e-4:
        mid = (bisect_left+bisect_right)/2
        clips, total = common.makeRanges(
            [(score[i] > mid) for i in range(n_frame)], len_min, len_max)
        if total/n_frame > ratio:
            bisect_left = mid
        else:
            bisect_right = mid

    # 区间列表生成
    threshold = bisect_left
    clips, total = common.makeRanges(
        [(score[i] > threshold) for i in range(n_frame)], len_min, len_max)
    print("  extractor.danmu_density: report: ", threshold, total)

    # 片段输出
    export_clips(clips, score, bvid, frame_rate, tag)


#####################################################################################
#####################################################################################

def main(bvid):
    print("  extractor: prep...")

    common.wstat(bvid, 0+random.randint(0,5), ext=True)

    shotcuts = shotcut(bvid)

    cid = sqlQuery(
        "select cid from vinfo where bvid='{bvid}'".format(bvid=bvid))[0][0]
    danmus = sqlQuery(
        "select * from danmu where cid='{cid}'".format(cid=cid), isDict=True)

    common.wstat(bvid, 40+random.randint(0,20), ext=True)

    thread_handles=[]

    # 提取器总个数
    n_extractors=6

    for i in range(n_extractors):
        def A(ext_id):
            # 在这里接入您的 extractor
            if ext_id==0:
                extractor_sine(ext_id, bvid, danmus, shotcuts)
            elif ext_id==1:
                extractor_danmu_density(ext_id, bvid, danmus, shotcuts)
            elif ext_id==2:
                extractor_hot(ext_id, bvid, danmus, shotcuts)
            elif ext_id==3:
                extractor_love(ext_id, bvid, danmus, shotcuts)
            elif ext_id==4:
                extractor_shock(ext_id, bvid, danmus, shotcuts)
            elif ext_id==5:
                extractor_humor(ext_id, bvid, danmus, shotcuts)
        thread_handles.append(Thread(target=A, args=(i,)))
    for th in thread_handles: th.start()
    for th in thread_handles: th.join()

    common.wstat(bvid, 100, ext=True)