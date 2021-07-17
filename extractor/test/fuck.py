import sys
sys.path.append("..")
import json
import ffmpeg
import math
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal
import algorithm.danmu.density
import algorithm.common.sig
import algorithm.shotcut.shotcut
import control.xvidgen
import media.editor

def solveAll(bvid):
    duration = int(math.ceil(float(ffmpeg.probe("../../data/media/%s.mp4"%bvid)["format"]["duration"])))
    frame_rate = 24
    frame_total = int(math.ceil(duration*frame_rate))

    file_danmu = open("../../data/danmu/%s.danmu.json"%bvid,"r",encoding="utf-8")
    danmu_list = json.load(file_danmu)
    file_danmu.close()

    shotcut_list = algorithm.shotcut.shotcut.shotcut("../../data/media/%s.mp4"%bvid)

    density_s=algorithm.danmu.density.calcDanmuDensity(danmu_list, duration, Delta=7)
    density_l=algorithm.danmu.density.calcDanmuDensity(danmu_list, duration, Delta=25)
    density_p=[density_s[i]/(density_l[i]+1) for i in range(duration)]
    tans=[density_p[i] * math.sqrt(density_s[i]) for i in range(duration)]
    ans=[]
    for i in tans: ans+=[i]*24
    ans=ans[0:frame_total]
    ans=scipy.signal.savgol_filter(ans,239,3)  

    for shotcut in shotcut_list:
        if shotcut["transition"]=="cut":
            fid=shotcut["cut_frame"]
            if fid<frame_total: ans[fid]=0
            if fid>0: ans[fid-1]=0
        else:
            fid_l=shotcut["start_frame"]
            fid_r=shotcut["end_frame"]
            for i in range(fid_l-1,fid_r+1):
                if i>=0 and i<frame_total: ans[i]=0

    thres = algorithm.common.sig.getPropotionPoint(ans,0.1)
    bans = [(ans[i]>thres) for i in range(frame_total)]

    res=algorithm.common.sig.makeRanges(bans,72,360)

    for i in res:
        xvid=control.xvidgen.generateId()
        print("write",xvid)
        xvobj={"id":xvid, "bvid":bvid, "frame_begin":i[0], "frame_end":i[1], "src_type":0, "clip_type":0}
        file_json = open("../../data/extract/%s.json"%xvid,"w",encoding="utf-8")
        json.dump(xvobj,file_json, sort_keys=True, indent=4, separators=(',', ':'))
        file_json.close()
        media.editor.edit([{"filename":"../../data/media/%s.mp4"%bvid, "start":xvobj["frame_begin"]/frame_rate, "duration":(xvobj["frame_end"]-xvobj["frame_begin"])/frame_rate}],"../../data/output/%s.mp4"%xvid)

if __name__ == "__main__":
    solveAll("BV1Uv411v7mM")