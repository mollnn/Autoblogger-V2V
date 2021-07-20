import sys
sys.path.append("..")
import algorithm.shotcut.shotcut
import cv2driver
import cv2
from matplotlib import pyplot as plt
import ffmpeg
import json


bvid = "BV1BA411q7oy"
video_filename = "../../data/media/BV1BA411q7oy.mp4"
# f=open("../../tmp/BV1BA411q7oy.shotcut.json","w")
# json.dump(algorithm.shotcut.shotcut.shotcut("../../data/media/BV1BA411q7oy.mp4"),f,indent=4,separators=(',',': '))
# f.close()


f = open("../../tmp/BV1BA411q7oy.shotcut.json", "r")
shotcut_list = json.load(f)


video = cv2driver.readVideo(video_filename)
n_frame = len(video)

shotcut_flags = [0]*n_frame
for shotcut in shotcut_list:
    if shotcut["transition"] == "cut":
        shotcut_flags[shotcut["cut_frame"]] = 1
    else:
        for i in range(shotcut["start_frame"], shotcut["end_frame"]):
            shotcut_flags[i] = 2

output_video_filename="output.avi"
cv_writer=cv2.VideoWriter(output_video_filename,cv2.VideoWriter_fourcc(*'XVID'),24,(640,360),True)

for i in range(n_frame):
    try:
        frame = video[i]
        if shotcut_flags[i] == 1:
            cv2.putText(frame, 'cut', (0, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 5)
        elif shotcut_flags[i] == 2:
            cv2.putText(frame, 'gradual', (0, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 0), 5)
        cv_writer.write(frame)
    except Exception:
        print("error")
cv_writer.release()
