import cv2

def readVideo(videoname):
    capture = cv2.VideoCapture(videoname )
    ans=[]
    if capture.isOpened():
        while True:
            ret,img=capture.read() # img 就是一帧图片        
            ans.append(img)
            if not ret:break # 当获取完最后一帧就结束
    else:
        print('视频打开失败！')
    return ans

if __name__=="__main__":
    bvid="BV1BA411q7oy"
    video_filename="../../data/media/BV1BA411q7oy.mp4"
    video=readVideo(video_filename)
    print("Video read ok")
