import cv2

record = False

cap = cv2.VideoCapture(0)

if (cap.isOpened() == False): 
  print("Unable to read camera feed")

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print(frame_height,frame_width)

out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

while(True):
  ret, frame = cap.read()
  if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    break
  k = cv2.waitKey(1)
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  cv2.imshow('frame',gray)

    # press space key to start recording
  if k%256 == 32:
    record = ~record
    if record==False:
        # record = True
        print('recoding start') 
    else:
        # record=False
        print('recoding pause')
  if record:
    out.write(frame) 

    # press q key to close the program
  if k & 0xFF == ord('q'):
    break

 

cap.release()
out.release()

cv2.destroyAllWindows()