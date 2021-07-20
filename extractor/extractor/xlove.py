import os
import sys
sys.path.append("..")
import database.msql
import media.editor
import control.xvidgen
import control.jsonconfig
import algorithm.shotcut.shotcut
import algorithm.common.sig
import algorithm.danmu.sentiments
import algorithm.danmu.density
import scipy.signal
import numpy as np
import math
import ffmpeg
import json
from matplotlib import pyplot as plt
from cv2 import data


def mark(bvid, duration, frame_total, danmu_list, shotcut_list):
    # Output: ans: The mark of each frame. len(ans)==frame_total
    sql_ans = database.msql.query(control.jsonconfig.readConfig(
        "db_banime"), "select love from framelabel where bvid='%s' order by frame;" % bvid)
    ans = [i[0]*10 for i in sql_ans]
    ans += [0]*(frame_total-len(ans))
    ans = scipy.signal.savgol_filter(ans, 73, 3)
    ans = [max(i,0) for i in ans]
    ans = scipy.signal.savgol_filter(ans, 73, 3)
    ans = [max(i,0) for i in ans]
    return ans


def solve(bvid):
    print("extractor.xhumor: Hello ", bvid)
    duration = int(math.ceil(
        float(ffmpeg.probe("../../data/media/%s.mp4" % bvid)["format"]["duration"])))
    frame_rate = 24     # Forced
    frame_total = int(math.ceil(duration*frame_rate))

    print("extractor.xhumor: Read danmu and shotcut from database... ", bvid)
    cid = database.msql.query(
        control.jsonconfig.readConfig("dbname"), "select cid from Vinfo where bvid='%s'" % bvid)[0][0]
    danmu_list = database.msql.query(
        control.jsonconfig.readConfig("dbname"), "select * from Danmu where cid='%s'" % cid, isDict=True)
    shotcut_list = database.msql.query(
        control.jsonconfig.readConfig("dbname"), "select * from shotcut where bvid='%s'" % bvid, isDict=True)

    print("extractor.xhumor: Analysing...")

    mark_original = mark(bvid, duration, frame_total, danmu_list, shotcut_list)
    mark_final = mark_original

    for shotcut in shotcut_list:
        if shotcut["transition"] == "cut":
            fid = shotcut["cut_frame"]
            if fid < frame_total:
                mark_final[fid] = 0
            if fid > 0:
                mark_final[fid-1] = 0
        else:
            frame_id_l = shotcut["start_frame"]
            frame_id_r = shotcut["end_frame"]
            for i in range(frame_id_l-1, frame_id_r+1):
                if i >= 0 and i < frame_total:
                    mark_final[i] = 0

    threshold = algorithm.common.sig.getPropotionPoint(mark_final, 0.2)
    is_frame_good = [(mark_final[i] > threshold) for i in range(frame_total)]

    # Visualization
    # plt.plot(mark_original)
    # plt.plot(is_frame_good)
    # plt.show()

    result = algorithm.common.sig.makeRanges(is_frame_good, 72, 360)

    print("extractor.xhumor: writing...")
    for i in result:
        xvid = control.xvidgen.generateId()
        extraction_obj = {"id": xvid, "bvid": bvid,
                          "frame_begin": i[0], "frame_end": i[1], "src_type": 0, "clip_type": 1}
        media.editor.edit([{"filename": "../../data/media/%s.mp4" % bvid, "start": extraction_obj["frame_begin"]/frame_rate,
                          "duration":(extraction_obj["frame_end"]-extraction_obj["frame_begin"])/frame_rate}], "../../data/output/%s.mp4" % xvid, quiet=True)
        os.system("ffmpeg -i ../../data/output/%s.mp4 -r 24 -ss 00:00:00 -vframes 1 ../../data/poster/%s.jpg  -hide_banner -loglevel error" % (xvid, xvid))
        database.msql.query(control.jsonconfig.readConfig("dbname"), "INSERT INTO extraction (id, bvid, frame_begin, frame_end, src_type, clip_type) VALUES ('%s','%s',%d,%d,%d,%d);" % (
            extraction_obj["id"], extraction_obj["bvid"], extraction_obj["frame_begin"], extraction_obj["frame_end"], extraction_obj["src_type"], extraction_obj["clip_type"]))

    print("extractor.xhumor: OK!")


if __name__ == "__main__":
    solve("BV1Uv411v7mM")
