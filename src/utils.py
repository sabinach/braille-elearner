import os
import cv2
import json
import string
import random
import numpy as np
import speech_recognition as sr
from params import *


###----------- Audio -----------###

def speak(text):
    table = string.maketrans("","")
    cleaned_text = text.translate(table, string.punctuation) 
    os.system("say '{}'".format(cleaned_text))


def sphinx_api(recognizer, audio):
    # recognize speech using Sphinx
    parsed_audio = None
    try:
        parsed_audio = recognizer.recognize_sphinx(audio)
        print("Sphinx thinks you said: {}".format(parsed_audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return parsed_audio


def google_api(recognizer, audio):
    # recognize speech using Google Speech Recognition
    parsed_audio = None
    try:
        parsed_audio = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said: {}".format(parsed_audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return parsed_audio

###----------- JSON -----------###


def load_json(filepath):
    with open(filepath) as json_file:
        item = json.load(json_file)
    return item


def save_json(item, savepath):
    # Serializing json  
    json_object = json.dumps(item, indent = 4) 
      
    # Writing to sample.json 
    with open(savepath, "w") as outfile: 
        outfile.write(json_object) 


###----------- Symbols -----------###


def generate_symbols(braille_symbols, repeat=False):
    # generate/save random configuration of 10 braille symbols
    current_symbols = []
    for i in range(NUM_CELLS):
        key = random.choice(list(braille_symbols.keys()))
        if not repeat:
            while key in current_symbols:
                key = random.choice(list(braille_symbols.keys()))
        current_symbols.append(key)
    return current_symbols


def get_dot_locations(pushed_contours, dot_boundaries, peg_centers):

    curr_cell_dots = {}
    for (cX, cY) in peg_centers:
        for i in range(len(dot_boundaries)):
            top_left = dot_boundaries[i]["top_left"] # [x, y]
            bottom_right = dot_boundaries[i]["bottom_right"]
            # center within dot boundary -> name center to respective dot location
            if (cX > top_left[0] and cX < bottom_right[0]) and (cY > top_left[1] and cY < bottom_right[1]):
                cell = dot_boundaries[i]["cell"]
                dot = dot_boundaries[i]["dot"]

                # add dot to cell dictionary
                if cell not in curr_cell_dots:
                    curr_cell_dots[cell] = [dot]
                else:
                    curr_cell_dots[cell].append(dot)

                # no need to waste time looping through everything
                break

    return curr_cell_dots


def match_symbols(cell_dot_locations, current_symbols, braille_symbols):
    # sort to make it easier to compare
    for cell in cell_dot_locations:
        cell_dot_locations[cell].sort()

    # figure out what is the braille cell symbol
    identified_symbols = []
    for cell in cell_dot_locations:
        identified = False
        for symbols in braille_symbols:
            if cell_dot_locations[cell] == braille_symbols[symbols]:
                identified_symbols.append(symbols)
                identified = True
                break
        if not identified:
            identified_symbols.append(None)

    # explicit information on what was cells/symbols were correct/incorrect
    match_results = [] # (generated(str), identified(str), match(bool))
    for i in range(NUM_CELLS):
        generated_symbol = current_symbols[i] 
        identified_symbol = identified_symbols[i]
        match_results.append((generated_symbol, identified_symbol, generated_symbol==identified_symbol))

    return match_results


def is_matched(match_results):
    matched = all(result[-1] for result in match_results)
    return matched


def get_dividers(img, width, height):
    x_dividers = [0]
    curr_x = 0
    for i in range(NUM_CELLS):
        curr_x += width/NUM_CELLS
        x_dividers.append(curr_x)
    return x_dividers


###----------- Image -----------###


def show_image(img, img_text):
    # show image
    cv2.imshow(img_text, img)

    # wait for keypress to exit 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)


def save_image(img, savepath):
    cv2.imwrite(savepath, img)


def get_contours(img, area_threshold):
    # Our operations on the frame come here
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, 240, 255, 0) # (grayscale_image, threshold_value, maxVal, minVal)

    # Get contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # make sure contours exist
    if contours is []:
        return img

    # filter/identify pegs that have been pushed up
    filtered_contours = []
    for i in range(0, len(contours)):
        area = cv2.contourArea(contours[i])
        if area >= area_threshold:
            filtered_contours.append(contours[i])

    return img, thresh, filtered_contours


def get_center(img, contours):
    centers = []
    for contour in contours:
        # compute the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        centers.append((cX, cY))
    return centers


###----------- Image Manipulation -----------###


def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)


def concatenate_image(img_names, img_dir, extension='.png'):
    # add .png to end of each image name
    img_list = []
    for filename in img_names:
        img_path = img_dir + filename + extension
        img_list.append(cv2.imread(img_path))

    # contatenate imamges together horizontally
    concatenated_img = hconcat_resize_min(np.array(img_list))

    curr_x = 0
    height, width = concatenated_img.shape[:2]
    for i in range(NUM_CELLS-1):
        curr_x += width/NUM_CELLS
        cv2.line(concatenated_img, (curr_x, 0), (curr_x, height), BLACK, 3)

    return concatenated_img


