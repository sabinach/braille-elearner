import numpy as np
import cv2

VIDEO_PORT = 0

cap = cv2.VideoCapture(VIDEO_PORT)

# video settings
width  = int(cap.get(3)) # 1280
height = int(cap.get(4)) # 960

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    k = cv2.waitKey(1)
    if k & 0xFF == 27:
        break

    if frame is not None:
        # Display the resulting frame
        cv2.imshow('frame',frame)

    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)