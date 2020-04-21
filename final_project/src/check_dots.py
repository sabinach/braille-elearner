import sys
sys.path.insert(0, '..')

import numpy as np
import cv2          # Version 4.2.0
from params import *
import json

import os
path = os.getcwd() 
parent_dir = os.path.abspath(os.path.join(path, os.pardir))


SHOW_VIDEO = True 


def get_bounds():
    with open(parent_dir+'/json/dot_boundaries.json') as json_file:
        dot_boundaries = json.load(json_file)
    return dot_boundaries


def get_symbols():
    with open(parent_dir+'/json/braille_symbols.json') as json_file:
        braille_symbols = json.load(json_file)
    return braille_symbols


def get_current_symbols():
    with open(parent_dir+'/json/current_symbols.json') as json_file:
        current_symbols = json.load(json_file)
    return current_symbols


def get_contours(img, show_peg_contours=SHOW_PEG_CONTOURS):
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
        if area >= PEG_THRESHOLD:
            peg_pushed.append(contours[i])

    # debugging:
    if show_peg_contours: 
        cv2.drawContours(img, peg_pushed, -1, RED, 3)

    return img, thresh, peg_pushed


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


def read_cells(peg_pushed, dot_boundaries, peg_centers):

    curr_cell_dots = {}
    for (cX, cY) in peg_centers:
        for i in range(len(dot_boundaries)):
            top_left = dot_boundaries[i]["top_left"] # [x, y]
            bottom_right = dot_boundaries[i]["bottom_right"]
            if (cX > top_left[0] and cX < bottom_right[0]) and (cY > top_left[1] and cY < bottom_right[1]):
                cell = dot_boundaries[i]["cell"]
                dot = dot_boundaries[i]["dot"]

                if cell not in curr_cell_dots:
                    curr_cell_dots[cell] = [dot]
                else:
                    curr_cell_dots[cell].append(dot)

                break

    return curr_cell_dots


def match_symbols(curr_cell_dots, braille_symbols, current_symbols):
    for cell in curr_cell_dots:
        curr_cell_dots[cell].sort()

    identified_symbols = []
    for cell in curr_cell_dots:
        for symbols in braille_symbols:
            if curr_cell_dots[cell] == braille_symbols[symbols]:
                identified_symbols.append(symbols)
                break

    match_results = [] # (generated(str), identified(str), match(bool))
    for i in range(NUM_CELLS):
        generated = current_symbols[i] 
        identified = identified_symbols[i]
        match_results.append((generated, identified, generated==identified))

    return match_results


def is_matched(match_results):
    matched = all(result[-1] for result in match_results)
    return matched


def get_video(show_video=SHOW_VIDEO):

    cap = cv2.VideoCapture(VIDEO_PORT)

    while cv2.waitKey(200) & 0xFF != 27:
        # Capture frame-by-frame
        ret, frame = cap.read()
        width  = int(cap.get(3)) # 1280
        height = int(cap.get(4)) # 960

        # only show braille cells
        cropped = frame[CROP_HEIGHT:CROP_WIDTH, 0:width] # img[y:y+h, x:x+w]



        # Image to be shown
        img, thresh, peg_pushed = get_contours(cropped)
        
        dot_boundaries = get_bounds()
        braille_symbols = get_symbols()
        current_symbols = get_current_symbols()

        peg_centers = get_center(img, peg_pushed)
        curr_cell_dots = read_cells(peg_pushed, dot_boundaries, peg_centers)
        match_results = match_symbols(curr_cell_dots, braille_symbols, current_symbols)
        matched = is_matched(match_results)



        # Display the resulting frame
        if show_video:
            cv2.imshow('img', img)
            cv2.imshow('thresh', thresh)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    get_video()