import scipy 
import math

def calcDanmuDensity(danmu_list, duration, Delta=15):
    ans = [0]*duration
    for danmu in danmu_list:
        ans[max(0,min(duration-1,int(math.ceil(float(danmu["floattime"])))))]+=1
    ans=scipy.signal.savgol_filter(ans,Delta,3)  
    ans=[max(ans[i],0) for i in range(duration)]
    return ans
