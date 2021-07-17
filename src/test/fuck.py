import sys
sys.path.append("..")
import json
import ffmpeg
import math
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal
import time
import database.connectorSSHMySQL as msql
import random


bvid="BV1Uv411v7mM"

duration = int(math.ceil(float(ffmpeg.probe("../../data/media/%s.mp4"%bvid.format(bid=bvid))["format"]["duration"])))
frame_rate = 24
frame_total = int(math.ceil(duration*frame_rate))

file_danmu = open("../../data/danmu/%s.danmu.json"%bvid,"r",encoding="utf-8")
danmu_list = json.load(file_danmu)
file_danmu.close()

file_json = open("../../tmp/%s.shotcut.json"%bvid,"r",encoding="utf-8")
shotcut_list=json.load(file_json)
file_json.close()

def calcDanmuDensity(danmu_list, duration, Delta=15):
    ans = [0]*duration
    for danmu in danmu_list:
        ans[max(0,min(duration-1,int(math.ceil(float(danmu["time"])))))]+=1
    ans=scipy.signal.savgol_filter(ans,Delta,3)  
    ans=[max(ans[i],0) for i in range(duration)]
    return ans

density_s=calcDanmuDensity(danmu_list, duration, Delta=7)
density_l=calcDanmuDensity(danmu_list, duration, Delta=25)
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

def positionsBeyond(a, val):
    return [i for i in range(len(a)) if a[i]>=val]

def getPropotionPoint(a, prop):
    l=np.min(a)
    r=np.max(a)
    while abs(r-l) > 1e-4:
        mid=(l+r)/2
        tmp=len(positionsBeyond(a, mid))
        if tmp/len(a) > prop:
            l=mid
        else:
            r=mid
    return l

thres = getPropotionPoint(ans,0.1)
# print(thres)
# plt.stackplot([i for i in range(frame_total)],ans)
# plt.plot([thres]*len(ans))
# plt.show()

bans = [(ans[i]>thres) for i in range(frame_total)]

def makeRanges(a):
    ans=[]
    length=len(a)
    last=-2
    now=0
    for i in range(length):
        if bans[i]>0:
            if i==now+1:
                now=i
            else: 
                if last>-2:
                    dura=(now-last)/frame_rate
                    if 3<dura and dura<15:
                        ans+=[[last,now]]
                    last=-2
                else:
                    last=i
                    now=i
    return ans

res= makeRanges(ans)
print(res)

def generateId():
    # Return XV + n  len(n)=22  total_len=24
    return "XV"+str(int(math.floor(time.time()*1000000000000)+random.randint(0,1000000000))%10000000000000000000000)

print(generateId())

for i in res:
    xvid=generateId()
    xvobj={"id":xvid, "bvid":bvid, "frame_begin":i[0], "frame_end":i[1], "src_type":0, "clip_type":0}
    print(xvobj)