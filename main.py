import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import pycaw
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities


wCam,hCam=1280,720
detector=htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

volumeRange=volume.GetVolumeRange()
minvol=volumeRange[0]
maxvol=volumeRange[1]
vol=0
VolumeBar=400
volumePercent=0
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
ptime=0
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    list=detector.findPosition(img)
    if len(list)!=0:
       

        x1,y1=list[4][1],list[4][2]
        x2,y2=list[8][1],list[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(137,207,4),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(137,207,4),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(136, 164, 209),2)
        cv2.circle(img,(cx,cy),15,(137,207,4),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)

        vol=np.interp(length,[50,300],[minvol,maxvol])
        VolumeBar=np.interp(length,[50,300],[400,150])
        volumePercent=np.interp(length,[50,300],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,255),cv2.FILLED)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(VolumeBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volumePercent)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'FPS {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
    cv2.imshow("Img",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()