import cv2
import mediapipe as mp
import time

record = False

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw =mp.solutions.drawing_utils

if (cap.isOpened() == False): 
  print("Unable to read camera feed")

img_width = int(cap.get(3))
img_height = int(cap.get(4))

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (img_width,img_height),True) 

while(True):
  ret, img = cap.read()
  if not ret:
    print("Can't receive img (stream end?). Exiting ...")
    break
  k = cv2.waitKey(1)
  imRGB =cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  results= hands.process(imRGB)
#   print(results.multi_hand_landmarks)
  if results.multi_hand_landmarks:
    for handLms in results.multi_hand_landmarks:
      mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)


  cv2.imshow('img',img)

    # press space key to start recording
  if k%256 == 32:
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