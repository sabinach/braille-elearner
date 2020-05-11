import cv2
import time
import utils
from params import *

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent.parent)


def generate():
    # generate new symbol order
    braille_symbols = utils.load_json(filepath=root_dir+'/json/braille_symbols.json')
    current_symbols = utils.generate_symbols(braille_symbols=braille_symbols, repeat=False)
    utils.save_json(item=current_symbols, savepath=root_dir+"/json/current_symbols.json")

    # concatenate image together
    img = utils.concatenate_image(img_names=current_symbols, img_dir=root_dir+"/img/alphabet/")
    cv2.imshow("new symbols", img)
    utils.save_image(img=img, savepath=root_dir+"/img/current_symbols.png")

    return current_symbols


def setup_mode():

    # start camera
    cap = cv2.VideoCapture(VIDEO_PORT)

    # video settings
    width  = int(cap.get(3)) # 1280
    height = int(cap.get(4)) # 960

    # generate new cells
    current_symbols = generate()

    #utils.speak("Match the symbols shown in the image by pushing up the pegs from the bottom of the peg slate. When all boxes on the image are green, then press ENTER.")

    # Exit if ESC pressed
    while cv2.waitKey(200) & 0xFF != 27:

        # Capture frame-by-frame
        ret, frame = cap.read()

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
            for i in range(len(cell_matches)):
                cell = str(i)
                top_left = (cell_boundaries[cell]["1"]["x"]-length, cell_boundaries[cell]["1"]["y"]-length)
                bottom_right = (cell_boundaries[cell]["6"]["x"]+length, cell_boundaries[cell]["6"]["y"]+length)
                if cell_matches[i]: 
                    color = GREEN 
                else:
                    color = RED 
                cv2.rectangle(img, top_left, bottom_right, color, 2)

        cv2.imshow('Your symbols', img)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)



if __name__ == '__main__':
    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        setup_intro = "Generating new braille symbols..."
        utils.speak(setup_intro)

    #------- Setup Mode -------#
    setup_mode()

    # close pygame
    pygame.quit()

