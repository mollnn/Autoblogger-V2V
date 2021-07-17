import sys
sys.path.append("..")

import extractor.main
import download.biliMedia as bmedia
import download.biliDanmu as bdanmu

def Fuck(bvid):
    bmedia.getMP4ByBid(bvid, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")
    bdanmu.saveDanmuByBid(bvid)
    extractor.main.extract(bvid,0,0)

Fuck("BV1Aa4y1a7HP")
Fuck("BV1qW411C7Da")
Fuck("BV1Z4411Q7Dc")
Fuck("BV1zT4y1T7SD")
Fuck("BV1HE41177c1")
