import os
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
import sys
from matplotlib import pyplot as plt

from cv2 import data
sys.path.append("..")
# from matplotlib import pyplot as plt


def mark(bvid, duration, frame_total, danmu_list, shotcut_list):
    # Output: ans: The mark of each frame. len(ans)==frame_total
    media_file_name = "../../data/media/%s.mp4" % bvid
    density_narrow = algorithm.danmu.density.calcDanmuDensity(
        danmu_list, duration, Delta=5)
    density_wide = algorithm.danmu.density.calcDanmuDensity(
        danmu_list, duration, Delta=15)
    ratio = [density_narrow[i]/(density_wide[i]+0.1) for i in range(duration)]
    sentiments = algorithm.danmu.sentiments.calcDanmuSentiments(
        danmu_list, duration)
    ans_per_sec = [ratio[i] * math.sqrt(density_narrow[i]) *
            (0.5+0.5*math.sqrt(sentiments[i])) for i in range(duration)]
    ans = []
    for i in ans_per_sec:
        ans += [i]*24
    ans = ans[0:frame_total]
    ans = scipy.signal.savgol_filter(ans, 97, 3)
    return ans


def solve(bvid):
    print("extractor.naive: Hello ", bvid)
    duration = int(math.ceil(
        float(ffmpeg.probe("../../data/media/%s.mp4" % bvid)["format"]["duration"])))
    frame_rate = 24     # Forced
    frame_total = int(math.ceil(duration*frame_rate))

    print("extractor.naive: Read danmu and shotcut from database... ", bvid)
    cid = database.msql.query(
        control.jsonconfig.readConfig("dbname"), "select cid from Vinfo where bvid='%s'" % bvid)[0][0]
    danmu_list = database.msql.query(
        control.jsonconfig.readConfig("dbname"), "select * from Danmu where cid='%s'" % cid, isDict=True)
    shotcut_list = database.msql.query(
        control.jsonconfig.readConfig("dbname"), "select * from shotcut where bvid='%s'" % bvid, isDict=True)

    print("extractor.naive: Analysing...")

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

    threshold = algorithm.common.sig.getPropotionPoint(mark_final, 0.15)
    is_frame_good = [(mark_final[i] > threshold) for i in range(frame_total)]

    # Visualization
    # plt.plot(mark_original)
    # plt.plot(is_frame_good)
    # plt.show()

    result = algorithm.common.sig.makeRanges(is_frame_good, 72, 360)

    print("extractor.naive: writing...")
    for i in result:
        xvid = control.xvidgen.generateId()
        extraction_obj = {"id": xvid, "bvid": bvid,
                 "frame_begin": i[0], "frame_end": i[1], "src_type": 0, "clip_type": 0}
        media.editor.edit([{"filename": "../../data/media/%s.mp4" % bvid, "start": extraction_obj["frame_begin"]/frame_rate,
                          "duration":(extraction_obj["frame_end"]-extraction_obj["frame_begin"])/frame_rate}], "../../data/output/%s.mp4" % xvid, quiet=True)
        os.system("ffmpeg -i ../../data/output/%s.mp4 -r 24 -ss 00:00:00 -vframes 1 ../../data/poster/%s.jpg  -hide_banner -loglevel error" % (xvid, xvid))
        database.msql.query(control.jsonconfig.readConfig("dbname"), "INSERT INTO extraction (id, bvid, frame_begin, frame_end, src_type, clip_type) VALUES ('%s','%s',%d,%d,%d,%d);" % (
            extraction_obj["id"], extraction_obj["bvid"], extraction_obj["frame_begin"], extraction_obj["frame_end"], extraction_obj["src_type"], extraction_obj["clip_type"]))

    print("extractor.naive: OK!")


if __name__ == "__main__":
    solve("BV1Uv411v7mM")
