# 自定义 cutter

import scipy 
import math
from snownlp import SnowNLP
import numpy as np
import ffmpeg
import common
import editor
import os
import scipy.signal
import shotcut
from threading import Thread


# 用于评分算法示例的弹幕密度计算函数
# 您不需要关心该函数的具体实现
def calcDanmuDensity(danmu_list, duration, Delta=15):
    ans = [0]*duration
    for danmu in danmu_list:
        ans[max(0,min(duration-1,int(math.ceil(float(danmu["floattime"])))))]+=1
    ans=scipy.signal.savgol_filter(ans,Delta,3)  
    ans=[max(ans[i],0) for i in range(duration)]
    return ans


# 评分算法示例：使用弹幕密度进行评分
# 输入参数：视频 bvid，时长，总帧数，弹幕列表，转场列表（格式与数据库中一致）
# 返回值：对每一帧的评分，用列表表示，格式形如 [mark0, mark1, ..., markm] 其中 marki 表示对第 i 帧的评分
# 您不需要关心该函数的具体实现
def mark(bvid, duration, frame_total, danmu_list, shotcut_list):
    # Output: ans: The mark of each frame. len(ans)==frame_total
    media_file_name = "../data/media/%s.mp4" % bvid
    # 增强双窗口法
    density_narrow = calcDanmuDensity(danmu_list, duration, Delta=5)
    density_wide = calcDanmuDensity(danmu_list, duration, Delta=15)
    ratio = [density_narrow[i]/(density_wide[i]+0.1) for i in range(duration)]
    ans_per_sec = [ratio[i] * math.sqrt(density_narrow[i])  for i in range(duration)]
    # 上面是按秒计算的，内插成按帧计算的（历史遗留问题）
    ans = []
    for i in ans_per_sec:
        ans += [i]*24
    ans = ans[0:frame_total]
    # 稍微平滑一下
    ans = scipy.signal.savgol_filter(ans, 97, 3)
    return ans

# 从数据库中拉取已经计算的评分
def get_mark(bvid, duration, frame_total, danmu_list, shotcut_list, colname):
    # Output: ans: The mark of each frame. len(ans)==frame_total
    sql_ans = common.query(common.readConfig(
        "db_banime"), "select %s from framelabel where bvid='%s' order by frame;" % (colname,bvid))
    ans = [i[0]*10 for i in sql_ans]
    ans += [0]*(frame_total-len(ans))
    ans = scipy.signal.savgol_filter(ans, 73, 3)
    ans = [max(i,0) for i in ans]
    return ans



######################################################################


# 对某个原始素材进行分割与评分，选取其中优质部分装入素材库
def solve(bvid, src_type):
    print("cutter: Hello ", bvid)

    # if len(common.query(common.readConfig("dbname"), """
    #     select * from extraction where bvid='{bvid}' and src_type='{src_type}' and clip_type='{clip_type}'
    #     """.format(bvid=bvid, src_type=src_type, clip_type=clip_type))) > 0:
    #     print("extractor.main.extract: Already extracted with same bvid, src_type and clip_type. Terminated.")
    #     return

    # 读取视频基本信息
    duration = int(math.ceil(
        float(ffmpeg.probe("../data/media/%s.mp4" % bvid)["format"]["duration"])))
    frame_rate = 24     # Forced
    frame_total = int(math.ceil(duration*frame_rate))

    # 读取视频附加信息
    cid = common.query(
        common.readConfig("dbname"), "select cid from Vinfo where bvid='%s'" % bvid)[0][0]
    danmu_list = common.query(
        common.readConfig("dbname"), "select * from Danmu where cid='%s'" % cid, isDict=True)
    shotcut_list = shotcut.shotcut(bvid)

    # 利用各种评分器进行评分
    for i in range(0,4):
        clip_type=i
        print("cutter: analysing...", bvid, "clip_type:",i)

        # 你可以在这里引用自己的评分器
        # 这是您需要添加修改的部分，您不需要关心本函数其它部分的具体实现细节
        if i==0:
            mark_original = mark(bvid, duration, frame_total, danmu_list, shotcut_list)
        elif i==1:
            mark_original=get_mark(bvid, duration, frame_total, danmu_list, shotcut_list, 'love')
        elif i==2:
            mark_original=get_mark(bvid, duration, frame_total, danmu_list, shotcut_list, 'shock')
        elif i==3:
            mark_original=get_mark(bvid, duration, frame_total, danmu_list, shotcut_list, 'humor')

        # 处理拉取失败的情况
        if np.max(mark_original)<0.0001:
            print("cutter: skip clip_type", clip_type)
            continue

        # mark_original 格式形如 [mark0, mark1, ..., markm] 其中 marki 表示对第 i 帧的评分

        # 将镜头分割的结果应用到评分上
        mark_final = mark_original
        for sc in shotcut_list:
            if sc["transition"] == "cut":
                # 处理直接转场
                fid = sc["cut_frame"]
                if fid < frame_total:
                    mark_final[fid] = 0
                if fid > 0:
                    mark_final[fid-1] = 0
            else:
                # 处理渐变转场（这里当作两次直接转场处理）
                frame_id_l = sc["start_frame"]
                frame_id_r = sc["end_frame"]
                for i in range(frame_id_l-1, frame_id_r+1):
                    if i >= 0 and i < frame_total:
                        mark_final[i] = 0

        # 目标提取比例，时长要求（现在的提取比例是考虑了时长要求后的提取比例）
        ratio=0.8
        dura_min=1*24
        dura_max=20*24

        # 二分法确定阈值
        l=np.min(mark_final)+0.001
        r=np.max(mark_final)
        while abs(r-l)>1e-4:
            mid=(l+r)/2
            is_frame_good = [(mark_final[i] > mid) for i in range(frame_total)]
            result, total = common.makeRanges(is_frame_good, dura_min, dura_max)
            if total/frame_total > ratio:
                l=mid
            else:
                r=mid
        print("threshold =",l)

        # 计算结果区间
        threshold = l
        is_frame_good = [(mark_final[i] > threshold) for i in range(frame_total)]
        result, total = common.makeRanges(is_frame_good, dura_min, dura_max)

        # result 格式形如 [[start_1,end_1], [start_2,end_2], ...]，单位为帧
        # 生成视频片段并将信息写入数据库
        print("cutter: writing...", bvid)
        def _solve_xvid(xvid):
            # 计算分数最大的位置和最大值
            score_maxpos=np.argmax(mark_final[i[0]:i[1]])+i[0]
            score_maxval=np.max(mark_final[i[0]:i[1]])
            extraction_obj = {"id": xvid, "bvid": bvid,
                    "frame_begin": i[0], "frame_end": i[1], "src_type": src_type, "clip_type": clip_type, "score_maxpos":score_maxpos, "score_maxval":score_maxval}
            # 生成 SD 和 HD 两个版本的 XV 文件
            editor.edit([{"filename": "../data/media/%s.mp4" % bvid, "start": extraction_obj["frame_begin"]/frame_rate,
                            "duration":(extraction_obj["frame_end"]-extraction_obj["frame_begin"])/frame_rate}], "../data/output/%s.mp4" % xvid, quiet=True)
            editor.edit([{"filename": "../data/media/%s.hd.mp4" % bvid, "start": extraction_obj["frame_begin"]/frame_rate,
                            "duration":(extraction_obj["frame_end"]-extraction_obj["frame_begin"])/frame_rate}], "../data/output/%s.hd.mp4" % xvid, quiet=True)
            # 生成 XV 的封面
            os.system("ffmpeg -i ../data/output/%s.mp4 -r 24 -ss 00:00:00 -vframes 1 ../data/poster/%s.jpg  %s" % (xvid, xvid, common.readConfig("ffmpeg_default")+common.readConfig("ffmpeg_quiet")))
            # 将条目写入数据库
            common.query(common.readConfig("dbname"), "INSERT ignore INTO extraction (id, bvid, frame_begin, frame_end, src_type, clip_type, score_maxpos, score_maxval) VALUES ('%s','%s',%d,%d,%d,%d,%d,%f);" % (
                extraction_obj["id"], extraction_obj["bvid"], extraction_obj["frame_begin"], extraction_obj["frame_end"], extraction_obj["src_type"], extraction_obj["clip_type"], extraction_obj["score_maxpos"], extraction_obj["score_maxval"]))

        # 并行生成各视频片段
        handles=[]
        for i in result:
            xvid = common.generateXvid()
            th=Thread(target=_solve_xvid, args=(xvid,))
            th.start()
            handles.append(th)
        for i in handles:
            i.join()

    print("cutter: OK!", bvid)
