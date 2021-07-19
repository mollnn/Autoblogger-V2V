import sys
sys.path.append("..")

import os
import re
import json

import network.myhtml as myhtml

def importMP4(video_id, input_filename, ffmpeg_config="-c:v copy -c:a aac -strict experimental"):
    os.system('ffmpeg -y -i ' + input_filename + ' ' + ffmpeg_config + ' ../../data/media/'+video_id+'.mp4  -hide_banner -loglevel error')
    print("Succeed! :)")


if __name__ == "__main__":  
    print("ok")
    importMP4("BV1Uv411v7mM")
