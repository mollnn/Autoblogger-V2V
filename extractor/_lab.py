import cv2
import common
from matplotlib import pyplot as plt
import ffmpeg
import json
import numpy as np
import wave
import scipy.signal as signal
import os

bvid = "BV1BA411q7oy"
video_filename = "../../data/media/BV1BA411q7oy.mp4"
# f=open("../../tmp/BV1BA411q7oy.shotcut.json","w")
# json.dump(algorithm.shotcut.shotcut.shotcut("../../data/media/BV1BA411q7oy.mp4"),f,indent=4,separators=(',',': '))
# f.close()



output_filename="../data/media/black.hd.avi"
output_video_filename="../data/media/black.onlyvideo.avi"
cv_writer=cv2.VideoWriter(output_video_filename,cv2.VideoWriter_fourcc(*'XVID'),24,(320,180),True)

n_frame=24*60

frame = [[[0]*3]*320]*180
f=np.array(frame,np.uint8)
for i in range(n_frame):
    cv_writer.write(f)
cv_writer.release()

output_audio_filename = "../data/media/black.onlyaudio.mp3"
fp = wave.Wave_write(output_audio_filename)
framerate = 44100
time = 60
t = np.arange(0, time, 1.0/framerate)
wave_data = signal.chirp(t, 100, time, 1000, method='linear') * 10000
wave_data = wave_data.astype(np.short)

fp.setframerate(44100)
fp.setnframes(60*44100)
fp.setnchannels(1)
fp.setsampwidth(2)
fp.writeframes(wave_data.tostring())
fp.close()

cmd = 'ffmpeg -i %s -i %s %s'%(output_video_filename,output_audio_filename,output_filename)
os.system(cmd)