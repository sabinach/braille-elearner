import sys
sys.path.insert(0, '../src/user/') # for utils.py, params.py

import cv2
from params import *

def get_video():

    # start camera
    cap = cv2.VideoCapture(VIDEO_PORT)

    # video settings
    width  = int(cap.get(3)) # 1280
    height = int(cap.get(4)) # 960

    while cv2.waitKey(200) & 0xFF != 27:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # only show braille cells
        cropped = frame[CROP_HEIGHT:CROP_WIDTH, 0:width] # img[y:y+h, x:x+w]

        # Display the resulting frame
        cv2.imshow('img', cropped)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    get_video()