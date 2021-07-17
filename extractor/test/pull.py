import sys
sys.path.append("..")

bvid="BV1Uv411v7mM"

import download.biliMedia as bmedia
import download.biliDanmu as bdanmu

bmedia.getMP4ByBid(bvid, ffmpeg_config="-c:v libx264 -c:a aac -vf scale=320:180 -r 24 -strict experimental -threads 4 -preset ultrafast")
bdanmu.saveDanmuByBid(bvid)
