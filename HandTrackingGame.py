import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

record = False
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()
if not cap.isOpened():
    print("Unable to read camera feed")
img_width = int(cap.get(3))
img_height = int(cap.get(4))

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (img_width, img_height), True)
while True:
    ret, img = cap.read()
    if not ret:
        print("Can't receive img (stream end?). Exiting ...")
        break
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        print(lmList[8])
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
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