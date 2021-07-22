import cv2
import common
from matplotlib import pyplot as plt
import ffmpeg
import json
import numpy as np


bvid = "BV1BA411q7oy"
video_filename = "../../data/media/BV1BA411q7oy.mp4"
# f=open("../../tmp/BV1BA411q7oy.shotcut.json","w")
# json.dump(algorithm.shotcut.shotcut.shotcut("../../data/media/BV1BA411q7oy.mp4"),f,indent=4,separators=(',',': '))
# f.close()



output_video_filename="../data/media/black.hd.avi"
cv_writer=cv2.VideoWriter(output_video_filename,cv2.VideoWriter_fourcc(*'XVID'),24,(1920,1080),True)

n_frame=24*60

frame = [[[0]*3]*1920]*1080
f=np.array(frame,np.uint8)
for i in range(n_frame):
    print(i)
    cv_writer.write(f)
cv_writer.release()
