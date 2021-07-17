import sys
sys.path.append("..")
import json
import shotcut.shotcut as shotcut

bvid="BV1Uv411v7mM"
shotcut_ans = shotcut.shotcut("../../data/media/%s.mp4"%bvid)

file_json = open("../../tmp/%s.shotcut.json"%bvid,"w",encoding="utf-8")
json.dump(shotcut_ans,file_json, sort_keys=True, indent=4, separators=(',', ':'))
file_json.close()