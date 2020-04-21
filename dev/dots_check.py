import sys
sys.path.insert(0, '../src/user/') # for utils.py, params.py

import os
import cv2 # Version 4.2.0np
import utils
from params import *

# get complete file name
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)


def get_video():

    # start camera
    cap = cv2.VideoCapture(VIDEO_PORT)

    # video settings
    width  = int(cap.get(3)) # 1280
    height = int(cap.get(4)) # 960

    while cv2.waitKey(200) & 0xFF != 27:
        # Capture frame-by-frame
        ret, frame = cap.read()

        ###-----------------------------------------###

        # only show braille cells
        cropped = frame[CROP_HEIGHT:CROP_WIDTH, 0:width] # img[y:y+h, x:x+w]

        # Get contours
        img, thresh, pushed_contours = utils.get_contours(img=cropped, area_threshold=PEG_THRESHOLD)

        # draw contours
        cv2.drawContours(img, pushed_contours, -1, RED, 3)
        
        # get data
        dot_boundaries = utils.load_json(filepath=root_dir+"/json/dot_boundaries.json")
        braille_symbols = utils.load_json(filepath=root_dir+"/json/braille_symbols.json")
        current_symbols = utils.load_json(filepath=root_dir+"/json/current_symbols.json")

        # get center
        peg_centers = utils.get_center(img=img, contours=pushed_contours)

        # draw centers
        for (cX, cY) in peg_centers:
            cv2.circle(img, (cX, cY), 3, BLACK, -1)

        # get dictionary of cells with associated pushed-up dots ie. {0: [0, 1], 1: []...}
        cell_dot_locations = utils.get_dot_locations(pushed_contours, dot_boundaries, peg_centers)

        # check if the user's pegslate symbols match the system's internal symbols        
        match_results = utils.match_symbols(cell_dot_locations, current_symbols, braille_symbols)
        all_matched = utils.is_matched(match_results)



        ###-----------------------------------------###

        # Display the resulting frame
        cv2.imshow('img', img)
        cv2.imshow('thresh', thresh)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    get_video()

    