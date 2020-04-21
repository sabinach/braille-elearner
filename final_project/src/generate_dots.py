import sys
sys.path.insert(0, '..')
from params import *
import json
import random
import cv2
import numpy as np

import os
path = os.getcwd() 
parent_dir = os.path.abspath(os.path.join(path, os.pardir))


def get_symbols():
    with open(parent_dir+'/json/braille_symbols.json') as json_file:
        braille_symbols = json.load(json_file)
    return braille_symbols


def save_current_symbols(current_symbols):
	# Serializing json  
    json_object = json.dumps(current_symbols, indent = 4) 
      
    # Writing to sample.json 
    with open(parent_dir+"/json/current_symbols.json", "w") as outfile: 
        outfile.write(json_object) 


def generate_dots(braille_symbols, save, repeat=False):
	# generate/save random configuration of 10 braille symbols
	current_symbols = []
	for i in range(NUM_CELLS):
		key = random.choice(list(braille_symbols.keys()))
		if not repeat:
			while key in current_symbols:
				key = random.choice(list(braille_symbols.keys()))
		current_symbols.append(key)
	if save:
		save_current_symbols(current_symbols)
	return current_symbols


def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)


def concatenate_image(current_symbols, save, show, extension='.png'):

	# add .png to end of each symbol
	symbol_images = []
	for symbol in current_symbols:
		img_path = parent_dir + '/img/alphabet/' + symbol + extension
		symbol_images.append(cv2.imread(img_path))

	# contatenate imamges together horizontally
	concatenated_img = hconcat_resize_min(np.array(symbol_images))

	curr_x = 0
	height, width = concatenated_img.shape[:2]
	for i in range(NUM_CELLS-1):
		curr_x += width/NUM_CELLS
		cv2.line(concatenated_img, (curr_x, 0), (curr_x, height), RED, 3)

	# save image
	if save:
		save_path = parent_dir + '/img/current_symbols.png'
		cv2.imwrite(save_path, concatenated_img)

	# show image
	if show:
		cv2.imshow('concatenated_img', concatenated_img)

		# wait for keypress to exit 
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		cv2.waitKey(1)



if __name__ == '__main__':
	#braille_symbols = get_symbols()
    #current_symbols = generate_dots(braille_symbols, save=True, repeat=False)

    current_symbols = ["r", "c", "f", "s", "l", "t", "b", "z", "j", "d"]
    concatenate_image(current_symbols, save=True, show=True)


