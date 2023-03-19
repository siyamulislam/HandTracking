import cv2
import time
import os
import HandTrackingModule as htm
wCam, hCam = 640, 480
pTime=0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = "FingerImages"
myList = os.listdir(folderPath)
# print(myList)
overlayList = []
for imgPath in myList:
    image =cv2.imread(f'{folderPath}/{imgPath}')
    image = cv2.resize(image, (200, 200))
    # print(f'{folderPath}/{imgPath}')
    overlayList.append(image)
# print(len(overlayList))
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4,8,12,16,20]

while True:
    success, img = cap.read()
    # img = cv2.flip(img, 1)
    lmList =detector.findPosition(img, draw=False)
    img =detector.findHands(img)
    h,w,c=overlayList[0].shape
    # print(lmList)
    if len(lmList)!=0:
        fingers =[]
         #thumb
        if lmList[tipIds[0]][1]>lmList[tipIds[4]][1]:
            # print('right' ,lmList[tipIds[0]][1], lmList[tipIds[4]][1])
            fingers.append(1) if lmList[tipIds[0]][1]>lmList[tipIds[0]-1][1] else fingers.append(0)
        else:
            # print('left' ,lmList[tipIds[0]][1], lmList[tipIds[4]][1])
            fingers.append(1) if lmList[tipIds[0]][1]<lmList[tipIds[0]-1][1] else fingers.append(0)
    
        #4 fingers
        for id in range(1,5):  
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFinger= fingers.count(1)
        img[0:h,0:w] = overlayList[totalFinger-1]
        # print(totalFinger)
        cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img, f'{totalFinger}',(45,375),cv2.FONT_HERSHEY_COMPLEX,5,(255,0,0),20)
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,3, (0,255, 0), 3)
    cv2.imshow("Image", img)
    k = cv2.waitKey(1)
    # press space key to start recording
    if k & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
