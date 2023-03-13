import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon,
                                        self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, handID=8, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            seletedhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(seletedhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    if id == handID:
                        cv2.circle(img, (cx, cy), 8, (24, 255, 0), cv2.FILLED)

        return lmList


def main():
    record = False
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
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
        lmList = detector.findPosition(img)

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


if __name__ == "__main__":
    main()
