import numpy as np

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

def makeRanges(bans, lim_min, lim_max):
    ans=[]
    length=len(bans)
    last=-2
    now=0
    for i in range(length):
        if bans[i]>0:
            if i==now+1:
                now=i
            else: 
                if last>-2:
                    dura=now-last
                    if lim_min<dura and dura<lim_max:
                        ans+=[[last,now]]
                    last=-2
                else:
                    last=i
                    now=i
    return ans