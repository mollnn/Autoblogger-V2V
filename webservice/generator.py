# 自定义 generator

import os
import common
import editor
import shotcut
import math
import ffmpeg


def generate(bvid, src_type, clip_type):
    # 以 bvid 作为模板，以类型为 (src_type, clip_type) 的所有片段作为素材，生成视频

    # 获取基本信息
    output_video_id = common.generateOvid()
    target_video_filename = "../data/media/%s.mp4" % bvid
    duration = int(math.ceil(
        float(ffmpeg.probe("../data/media/%s.mp4" % bvid)["format"]["duration"])))
    frame_rate = 24     # Forced
    count_frame = int(math.ceil(duration*frame_rate))

    # 分析模板视频中的转场情况
    shotcut_list = shotcut.shotcut(bvid)
    shotcut_tag = [0]*count_frame
    for shot_cut in shotcut_list:
        if shot_cut["transition"] == "cut":
            shotcut_tag[min(count_frame-1, shot_cut["cut_frame"])] = 1
        else:
            shotcut_tag[min(count_frame-1, shot_cut["start_frame"])] = 2
            shotcut_tag[min(count_frame-1, shot_cut["end_frame"])] = 3

    # 生成剪辑描述（视频文件待定）
    edit_description = []
    last_cut_frame = 0
    for frame_id in range(count_frame):
        try:
            if shotcut_tag[frame_id] > 0:
                clip_begin = last_cut_frame
                clip_end = frame_id
                clip_duration = frame_id-last_cut_frame
                clip_desc = {"xvid": "", "start": 0,
                             "duration": clip_duration/24}
                edit_description.append(clip_desc)
                last_cut_frame = frame_id
        except Exception:
            print("error")

    # 选择合适的视频片段填入剪辑描述中
    for frame_id in edit_description:
        sql_result = common.query(common.readConfig(
            "dbname"), "select id from extraction where src_type=%d and clip_type=%d and frame_end-frame_begin>%d+1 order by rand() limit 1;" % (src_type, clip_type, int(frame_id["duration"]*24)))
        if len(sql_result) > 0:
            frame_id["xvid"] = sql_result[0][0]

    # 将剪辑描述写入数据库中
    id = 0
    for frame_id in edit_description:
        common.query(common.readConfig("dbname"), "insert ignore into out_editdesc (ovid, id, xvid, start, duration) values ('%s',%d,'%s',%f,%f)" % (
            output_video_id, id, frame_id["xvid"], frame_id["start"], frame_id["duration"]))
        id += 1
    common.query(common.readConfig(
        "dbname"), "insert ignore into out_template (ovid, bvid) values ('%s','%s')" % (output_video_id, bvid))
    return output_video_id
