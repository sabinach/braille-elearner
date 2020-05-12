# coding: utf-8

#import sys
#sys.path.insert(0, '..') # REVERT

import cv2
import time
import utils
from params import *

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)

# get min/max x bounds
MIN_X, MAX_X, NUM_CELLS, CELL_LENGTH = utils.get_leap_boundaries(filepath=root_dir+"/json/leap_boundaries.json")


def generate(width, height):
    # generate new symbol order
    braille_symbols = utils.load_json(filepath=root_dir+'/json/braille_symbols.json')
    current_symbols = utils.generate_symbols(braille_symbols=braille_symbols, repeat=False)
    utils.save_json(item=current_symbols, savepath=root_dir+"/json/current_symbols.json")

    # concatenate image together
    img = utils.concatenate_image(img_names=current_symbols, img_dir=root_dir+"/img/alphabet/")

    # resize image
    dim = (width, height)
    img = cv2.resize(img, dim)

    # show new generated image symbols
    utils.save_image(img=img, savepath=root_dir+"/img/current_symbols.png")

    return current_symbols, img


def setup_mode():

    # start camera
    cap = cv2.VideoCapture(VIDEO_PORT)

    # video settings
    width  = int(cap.get(3)) # 1280
    height = int(cap.get(4)) # 960

    # generate new cells
    current_symbols, img_symbols = generate(width=width, height=CROP_WIDTH-CROP_HEIGHT)

    # current cell
    current_cell = 0

    # get dot symbols of all braille symbols
    braille_symbols = utils.load_json(filepath=root_dir+'/json/braille_symbols.json')
    current_symbols = utils.load_json(filepath=root_dir+'/json/current_symbols.json')

    # Exit if ESC or DELETE pressed
    while True:

        key = cv2.waitKey(1)
        if key & 0xFF == 27 or key == 127: # ESC, delete
            utils.speak("Exiting set up")
            break

        # Capture frame-by-frame
        ret, frame = cap.read()

        if frame is not None:

            # only show braille cells
            cropped = frame[CROP_HEIGHT:CROP_WIDTH, 0:width] # img[y:y+h, x:x+w]

            # Get contours
            img, thresh, pushed_contours = utils.get_contours(img=cropped, area_threshold=PEG_THRESHOLD)

            # draw contours
            cv2.drawContours(img, pushed_contours, -1, BLUE, 3)

            # get data
            dot_boundaries = utils.load_json(filepath=root_dir+"/json/dot_boundaries.json")
            cell_boundaries = utils.load_json(filepath=root_dir+"/json/cell_boundaries.json")
            braille_symbols = utils.load_json(filepath=root_dir+"/json/braille_symbols.json")
            current_symbols = utils.load_json(filepath=root_dir+"/json/current_symbols.json")
            
            # get center
            peg_centers = utils.get_center(img=img, contours=pushed_contours)

            '''
            # draw centers
            for (cX, cY) in peg_centers:
                cv2.circle(img, (cX, cY), 3, BLACK, -1)
            '''

            # get dictionary of cells with associated pushed-up dots ie. {0: [0, 1], 1: []...}
            cell_dot_locations = utils.get_dot_locations(pushed_contours, dot_boundaries, peg_centers)

            if len(cell_dot_locations) == NUM_CELLS:

                # check if the user's pegslate symbols match the system's internal symbols        
                match_results = utils.match_symbols(cell_dot_locations, current_symbols, braille_symbols)
                cell_matches = [result[2] for result in match_results]

                length = 30
                all_match = True
                for i in range(len(cell_matches)):
                    cell = str(i)
                    top_left = (cell_boundaries[cell]["1"]["x"]-length, cell_boundaries[cell]["1"]["y"]-length)
                    bottom_right = (cell_boundaries[cell]["6"]["x"]+length, cell_boundaries[cell]["6"]["y"]+length)
                    if cell_matches[i]: 
                        color = GREEN 
                    else:
                        color = RED 
                        all_match = False
                    cv2.rectangle(img, top_left, bottom_right, color, 2)

                # left
                if key == 2:
                    current_cell -= 1
                    if current_cell == -1:
                        current_cell = NUM_CELLS - 1

                    if cell_matches[current_cell]:
                        utils.speak("Cell {}: Matched".format(current_cell))
                    else:
                        utils.speak("Cell {}: NOT matched".format(current_cell))

                # right
                elif key == 3:
                    current_cell += 1
                    if current_cell == NUM_CELLS-1:
                        current_cell = 0

                    if cell_matches[current_cell]:
                        utils.speak("Cell {}: Matched".format(current_cell))
                    else:
                        utils.speak("Cell {}: NOT matched".format(current_cell))

                # space
                elif key == 32:
                    generated, identified, matched = match_results[current_cell]
                    dot_numbers_list = braille_symbols[generated]
                    if len(dot_numbers_list) > 1: dot_numbers_list.insert(-1, "and")
                    dot_numbers_string = ','.join(map(str, dot_numbers_list))
                    print("Cell {}, Push up dots: {}".format(current_cell, dot_numbers_list))
                    utils.speak("Cell {}: , Push up dots: {}".format(current_cell, dot_numbers_string))

                # set-up done -- start user mode!
                if all_match:
                    print("Set Up DONE")
                    break

                # reset key to prevent duplicate
                key = None

            
            # left
            if key == 2:
                current_cell -= 1
                if current_cell == -1:
                    current_cell = NUM_CELLS - 1
                utils.speak("Cell {}".format(current_cell))

            # right
            elif key == 3:
                current_cell += 1
                if current_cell == NUM_CELLS-1:
                    current_cell = 0
                utils.speak("Cell {}".format(current_cell))

            # space
            elif key == 32:
                dot_numbers_list = braille_symbols[current_symbols[current_cell]]
                if len(dot_numbers_list) > 1: dot_numbers_list.insert(-1, "and")
                dot_numbers_string = ','.join(map(str, dot_numbers_list))
                print("Cell {}, Push up dots: {}".format(current_cell, dot_numbers_list))
                utils.speak("Cell {}: , Push up dots: {}".format(current_cell, dot_numbers_string))


            img_v = cv2.vconcat([img_symbols, img])
            cv2.imshow('Peg Slate Set Up', img_v)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    return all_match



if __name__ == '__main__':
    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        setup_intro = "Generating new braille symbols..."
        utils.speak(setup_intro)

    #------- Setup Mode -------#

    setup_mode()


