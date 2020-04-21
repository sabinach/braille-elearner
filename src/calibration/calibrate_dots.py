import sys
sys.path.insert(0, '../user') # for utils.py, params.py

import cv2          # Version 4.2.0
import json
import numpy as np

import utils
from params import *

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent.parent)


def number_pegs(img, peg_centers, x_dividers, show_peg_bounds):

    peg_color = {0: (53, 211, 81), 1: (13, 23, 143), 2: (69, 121, 215), 3: (165, 78, 248), 4: (83, 207, 204), 5: (185, 240, 217), 6: (136, 220, 14)}

    center_identifiers = {}
    dot_boundaries = []

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

    
    # color pegs based on color
    if show_peg_bounds:
        length = 20
        for center in center_identifiers:
            cell = center_identifiers[center]["cell"]
            dot = center_identifiers[center]["dot"]
            (cX, cY) = center

            dot_boundaries.append({  "cell": cell, 
                                        "dot": dot, 
                                        "top_left": (cX-length, cY-length), 
                                        "bottom_right": (cX+length, cY+length)
                                    }) 

            cv2.rectangle(img, (cX-length, cY-length), (cX+length, cY+length), peg_color[dot], 2)

    return dot_boundaries



def get_video():

    print("Press ESC to save dot calibration")

    cap = cv2.VideoCapture(VIDEO_PORT)

    while cv2.waitKey(200) & 0xFF != 27:
        # Capture frame-by-frame
        ret, frame = cap.read()
        width  = int(cap.get(3)) # 1280
        height = int(cap.get(4)) # 960

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
        dot_boundaries = number_pegs(img, peg_centers, x_dividers, show_peg_bounds=SHOW_PEG_BOUNDS)

        ###-----------------------------------------###

        # Display the resulting frame
        cv2.imshow('img', img)
        cv2.imshow('thresh', thresh)


    # Save calibrated dot boundaries
    utils.save_json(dot_boundaries, savepath=root_dir+"/json/dot_boundaries.json")


    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    get_video()