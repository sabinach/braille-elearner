import sys
sys.path.insert(0, '../src/user/') # for utils.py, params.py

from params import *
import utils

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)


if __name__ == '__main__':
    # generate new symbol order
    braille_symbols = utils.load_json(filepath=root_dir+'/json/braille_symbols.json')
    current_symbols = utils.generate_symbols(braille_symbols=braille_symbols, repeat=False)
    utils.save_json(item=current_symbols, savepath=root_dir+"/json/current_symbols.json")

    #current_symbols = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

    # concatenate image together
    img = utils.concatenate_image(img_names=current_symbols, img_dir=root_dir+"/img/alphabet/")
    utils.show_image(img=img, img_text="new symbols")
    utils.save_image(img=img, savepath=root_dir+"/img/current_symbols.png")



