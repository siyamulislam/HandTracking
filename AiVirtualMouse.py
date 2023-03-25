import cv2
import numpy as np
import time
import HandTrackingModule as htm
import autopy

######################
wCam, hCam = 640, 480
pTime = 0
frameR=120#frame Reduction
smoothening = 5 
plocX, plocY = 0, 0
clocX, clocY = 0, 0
######################
cap = cv2.VideoCapture(1)
if (cap.isOpened() == False):
    print("Unable to read camera feed")
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr,hScr =autopy.screen.size()

while True:
    ret, img = cap.read()
    if not ret:
        print("Can't receive img (stream end?). Exiting ...")
        break
    # 1 Find Hand landmarks
    img= cv2.flip(img,1)
    lmList = detector.findPosition(img,drawItems=[8])
    img = detector.findHands(img)
    # 2. Get the tip of the index and middle fingers

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # 3. Check Which Fingers Up
        fingers = detector.fingersUp()
        # print(fingers)
        # 4. Only Index Finger Moving Mode
        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,0),2)

        if fingers[1] and fingers[2]==False:
            # 5. Convert Coordinates
            x3= np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3= np.interp(y1,(frameR,hCam-frameR),(0,hScr))
            # print(x3,y3)
            # 6. Smoothen Values
            clocX = plocX +(x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            autopy.mouse.move(clocX,clocY)
            # cv2.circle(img,(x1,y1),10,drawColor,cv2.FILLED)
            plocX,plocY=clocX,clocY
        # 8. Both Index and middle fingers are up: Clicking Mode
        if fingers[1] and fingers[2]:
            # 9. Find distance between fingers
            length,img,lineInfo= detector.findDistance(8,12,img)
            # print(length)
            # 10. Click mouse if distance short
            if length <40:
                cv2.circle(img,(lineInfo [4], lineInfo[5]), 10, (255, 0,0 ), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'{int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    cv2.imshow('Image', img)
    k = cv2.waitKey(1)

    if k & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
