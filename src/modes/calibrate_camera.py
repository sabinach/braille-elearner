#import sys
#sys.path.insert(0, '..') # for utils.py, params.py

import cv2          # Version 4.2.0
import json
import numpy as np

import utils
from params import *

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)

# get min/max x bounds
MIN_X, MAX_X, NUM_CELLS, CELL_LENGTH = utils.get_leap_boundaries(filepath=root_dir+"/json/leap_boundaries.json")


def number_pegs(img, peg_centers, x_dividers):

    center_identifiers = {}

    # cell
    cell_nums = {} 
    for (cX, cY) in peg_centers:
        for i in range(1, len(x_dividers)):
            if cX > x_dividers[i-1] and cX < x_dividers[i]:
                cell = i-1

                # for cell number
                if i-1 not in cell_nums:
                    cell_nums[cell] = [(cX, cY)]
                else:
                    cell_nums[cell].append((cX, cY))

                # identify centers
                center_identifiers[(cX, cY)] = {"cell": i-1}

                break


    # dot
    for cell in cell_nums:
        initial_sort = sorted(cell_nums[cell] , key=lambda k: k[0])
        col1 = initial_sort[:3]
        col2 = initial_sort[3:]

        col1_sort = sorted(col1, key=lambda k: k[1])
        dot = 1
        for center in col1_sort:
            center_identifiers[center]["dot"] = dot
            dot += 1

        col2_sort = sorted(col2, key=lambda k: k[1])
        dot = 4
        for center in col2_sort:
            center_identifiers[center]["dot"] = dot
            dot += 1

    return center_identifiers



def get_video():

    print("Press SPACE (image focus) to save dot calibration")

    cap = cv2.VideoCapture(VIDEO_PORT)
    
    width  = int(cap.get(3)) # 1280
    height = int(cap.get(4)) # 960

    while cv2.waitKey(200) & (0xFF != 27) & (0xFF != 32): # ESC:27, SPACE:32 (ASCII-DEC)
        # Capture frame-by-frame
        ret, frame = cap.read()

        ###-----------------------------------------###

        # only show braille cells
        cropped = frame[CROP_HEIGHT:CROP_WIDTH, 0:width] # img[y:y+h, x:x+w]

        # Get contours
        img, thresh, pushed_contours = utils.get_contours(img=cropped, area_threshold=PEG_THRESHOLD)

        # draw contours
        cv2.drawContours(img, pushed_contours, -1, RED, 3)

        # get center
        peg_centers = utils.get_center(img=img, contours=pushed_contours)

        # draw centers
        for (cX, cY) in peg_centers:
            cv2.circle(img, (cX, cY), 3, BLACK, -1)

        # cell dividers (x-axis)
        x_dividers = utils.get_dividers(img, width, height)

        # draw cell dividers
        for curr_x in x_dividers:
            cv2.line(img, (curr_x, 0), (curr_x, height), BLUE, 3)

        # mark cell numbers
        center_identifiers = number_pegs(img, peg_centers, x_dividers)

        # color pegs
        length = 20
        dot_boundaries = []
        cell_boundaries = {}
        for center in center_identifiers:
            cell = center_identifiers[center]["cell"]
            dot = center_identifiers[center]["dot"]
            (cX, cY) = center
            dot_boundaries.append({ "cell": cell, 
                                    "dot": dot, 
                                    "top_left": (cX-length, cY-length), 
                                    "bottom_right": (cX+length, cY+length)
                                }) 
            cv2.rectangle(img, (cX-length, cY-length), (cX+length, cY+length), PEG_COLORS[dot], 2)

            if dot==1 or dot==6:
                if cell not in cell_boundaries:
                    cell_boundaries[cell] = {dot: {'x': cX, 'y': cY}}
                else:
                    cell_boundaries[cell][dot] = {'x': cX, 'y': cY}

        ###-----------------------------------------###

        # Display the resulting frame
        cv2.imshow('img', img)
        cv2.imshow('thresh', thresh)


    # Save calibrated dot and cell boundaries
    utils.save_json(dot_boundaries, savepath=root_dir+"/json/dot_boundaries.json")
    utils.save_json(cell_boundaries, savepath=root_dir+"/json/cell_boundaries.json")

    # debugging
    print("Saved dot calibration")

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    get_video()