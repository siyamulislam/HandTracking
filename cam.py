import cv2
import time
pTime=0

record = False

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False): 
  print("Unable to read camera feed")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(frame_height,frame_width)

# out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height),True)
out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc(*'DIVX'), 10, (frame_width,frame_height),True)

while(True):
  ret, frame = cap.read()
  if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    break
  k = cv2.waitKey(1)
  cTime=time.time()
  fps=1/(cTime-pTime)
  pTime=cTime

  cv2.putText(frame,str(int(fps)),(10,60),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)
  cv2.imshow('frame',frame)

    # press space key to start recording
  if k%256 == 32:
    record = ~record
    if record:
        # record = True
        print('recoding start') 
    else:
        # record=False
        print('recoding pause')
  if record:
    print('recoding frra,e')
    out.write(frame) 

    # press q key to close the program
  if k & 0xFF == ord('q'):
    break

 

cap.release()
out.release()

cv2.destroyAllWindows()