import sys
sys.path.append("..")

import shotcut
import database.msql

def doShotCut(bvid):
    ans=shotcut.shotcut(bvid)
    msql.query("biliextract","")