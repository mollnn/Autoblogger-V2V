import sys
sys.path.append("..")

import extractor.main
import download.biliMedia as bmedia
import download.biliDanmu as bdanmu

def Fuck(bvid):
    bmedia.getMP4ByBid(bvid, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")
    bdanmu.saveDanmuByBid(bvid)
    extractor.main.extract(bvid,0,1)

Fuck("BV1Gs411H7bf")
Fuck("BV1hx411e7KP")
Fuck("BV1QT4y1K7Ym")
Fuck("BV1Ub411w7zn")
