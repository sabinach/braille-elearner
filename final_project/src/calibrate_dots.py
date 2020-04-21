import sys
sys.path.insert(0, '..')

import numpy as np
import cv2          # Version 4.2.0
from params import *
import json

import os
path = os.getcwd() 
parent_dir = os.path.abspath(os.path.join(path, os.pardir))


def get_dividers(img, show_cell_dividers=SHOW_CELL_DIVIDERS):
    
    height = img.shape[0]
    width = img.shape[1]

    x_dividers = [0]
    curr_x = 0
    for i in range(NUM_CELLS):
        curr_x += width/NUM_CELLS
        x_dividers.append(curr_x)

        if show_cell_dividers:
            cv2.line(img, (curr_x, 0), (curr_x, height), BLUE, 3)

    return x_dividers


def get_center(img, peg_pushed, show_center=SHOW_CENTER):
    peg_centers = []
    for contour in peg_pushed:
        # compute the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        if show_center:
            cv2.circle(img, (cX, cY), 3, BLACK, -1)

        peg_centers.append((cX, cY))

    return peg_centers



def number_pegs(img, peg_centers, x_dividers):

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
    if SHOW_PEG_BOUNDS:
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


def identify_dots(img, show_peg_contours=SHOW_PEG_CONTOURS):
    # Our operations on the frame come here
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 240, 255, 0) # (grayscale_image, threshold_value, maxVal, minVal)

    # Get contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # make sure contours exist
    if contours is []:
        return img

    # filter/identify pegs that have been pushed up
    peg_pushed = []
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])
        if (area >= PEG_THRESHOLD):
            peg_pushed.append(contours[i])

    # debugging:
    if show_peg_contours: 
        cv2.drawContours(img, peg_pushed, -1, RED, 3)


    # cell dividers (x-axis)
    x_dividers = get_dividers(img)

    # peg centers
    peg_centers = get_center(img, peg_pushed)

    # mark cell numbers
    bound_identifiers = number_pegs(img, peg_centers, x_dividers)

    return img, thresh, bound_identifiers


def get_video():

    print("Press ESC to save dot calibration")

    cap = cv2.VideoCapture(VIDEO_PORT)

    while cv2.waitKey(200) & 0xFF != 27:
        # Capture frame-by-frame
        ret, frame = cap.read()
        width  = int(cap.get(3)) # 1280
        height = int(cap.get(4)) # 960

        # only show braille cells
        cropped = frame[CROP_HEIGHT:CROP_WIDTH, 0:width] # img[y:y+h, x:x+w]

        # Image to be shown
        img, thresh, dot_boundaries = identify_dots(cropped)

        # Display the resulting frame
        cv2.imshow('img', img)
        cv2.imshow('thresh', thresh)


    # Serializing json  
    json_object = json.dumps(dot_boundaries, indent = 4) 
      
    # Writing to sample.json 
    with open(parent_dir+"/json/dot_boundaries.json", "w") as outfile: 
        outfile.write(json_object) 

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    get_video()