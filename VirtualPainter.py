import cv2
import time
import os
import numpy as np
import HandTrackingModule as htm

wCam, hCam = 1280, 720
record = False
pTime = 0
folderPath= "Header"
myList= os.listdir(folderPath)
# print(myList)
overlayList=[]
for imPath in myList:
    image =cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
header =overlayList[0]
drawColor=(255,0,255)
brushThickness=15
eraserThickness=100
imgCanvas= np.zeros((720,1280,3),np.uint8)
xp,yp=0,0

cap = cv2.VideoCapture()
# cap = cv2.VideoCapture('input.avi')
if (cap.isOpened() == False):
    print("Unable to read camera feed")
cap.set(3, wCam)
cap.set(4, hCam)
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (wCam, hCam), True)
detector =htm.handDetector(0.70)

while (True):
    ret, img = cap.read()
    if not ret:
        print("Can't receive img (stream end?). Exiting ...")
        break
    img= cv2.flip(img,1)

    # find hand landmarks
    lmList =detector.findPosition(img, draw=False,drawItems=[8,12])
    img =detector.findHands(img, draw=True)
    if len(lmList)!=0:
        # tip of index and middle finger
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        # check up finger
        fingers=detector.fingersUp()
        # print(fingers)
        # if selection mode - Two finger are up
        if fingers[1] and fingers[2]:
            # print('sm')
            xp,yp=0,0
            if y1<125:
                if 200<x1<400:
                    header =overlayList[0]
                    drawColor=(255,0,255)
                elif 500<x1<700:
                    header =overlayList[1]
                    drawColor=(255,0,0)
                elif 750<x1<900:
                    header =overlayList[2]
                    drawColor=(0,255,0)
                elif 920<x1<1200:
                    header =overlayList[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y1+25),drawColor,cv2.FILLED)
 
        # if drawing mode - Index are up
        if fingers[1] and fingers[2]==False:
             # print('dm')
            cv2.circle(img,(x1,y1),10,drawColor,cv2.FILLED)
            if xp==0 and xp==0:
                xp,yp= x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)

            cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp= x1,y1
 
    imgGray= cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)

    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    img= cv2.bitwise_and(img,imgInv)
    img= cv2.bitwise_or(img,imgCanvas)

    # cv2.imshow('Imageg', imgInv)

    # setting header image
    img[0:125,0:wCam]=header
    # img= cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    #fps
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'{int(fps)}', (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
    cv2.imshow('Image', img)
    # cv2.imshow('Canvas', imgCanvas)
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
