import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
# wCam, hCam = 1280, 720
record = False
pTime = 0
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('input.avi')
if (cap.isOpened() == False):
    print("Unable to read camera feed")

cap.set(3, wCam)
cap.set(4, hCam)
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (wCam, hCam), True)

detector = htm.handDetector(detectionCon=0.80)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
volBar=400;volPer=0

while (True):
    ret, img = cap.read()
    if not ret:
        print("Can't receive img (stream end?). Exiting ...")
        break
    lmList = detector.findPosition(img, drawItems=[4, 8], draw=False)
    cv2.rectangle(img,(30,50),(60,400),(0,255,0),3)
    cv2.rectangle(img,(30,int(volBar)),(60,400),(0,255,0),cv2.FILLED)


    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        # print(x1,y1, x2,y2)
        cv2.circle(img, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        # cv2.circle(img, (cx, cy), 7, (0, 255, 255), cv2.FILLED)

        length = int(math.hypot(x2-x1, y2-y1))
        # hand range 30-300 | vol range -65-0

        vol=np.interp(length,[50,250],[minVol,maxVol])
        volBar=np.interp(length,[50,250],[400,50])
        volPer=np.interp(length,[50,250],[0,100])

        cv2.rectangle(img,(30,int(volBar)),(60,400),(0,255,0),cv2.FILLED)

        print(length,int(vol),int(volBar)) 
        volume.SetMasterVolumeLevel(vol, None)



        if length in range(0, 35):
            cv2.circle(img, (cx, cy), 7, (255, 255, 255), cv2.FILLED)
        elif length in range(35, 100):
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
        elif length in range(100, 160):
            cv2.circle(img, (cx, cy), 7, (0, 255, 255), cv2.FILLED)
        elif length in range(160, 300):
            cv2.circle(img, (cx, cy), 7, (0, 0, 255), cv2.FILLED)
        else:
            print("Value is outside the specified ranges")


    img = detector.findHands(img, draw=True)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (wCam-150, 30),  cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    cv2.putText(img, f'Vol:{int(volPer)}%', (10, 30),  cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow('img', img)

    k = cv2.waitKey(1)
    # press space key to start recording
    if k % 256 == 32:
        record = ~record
        if record:
            print('recoding start')
        else:
            print('recoding pause')
    if record:
        out.write(img)
        # press q key to close the program
    if k & 0xFF == ord('q'):
        break

cap.release()
out.release()

cv2.destroyAllWindows()
