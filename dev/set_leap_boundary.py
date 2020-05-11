import sys
sys.path.insert(0, '..') # for utils.py

import utils

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent.parent)

leap_boundaries = utils.load_json(filepath=root_dir+"/json/leap_boundaries.json")  
print(leap_boundaries[0]["CELL_LENGTH"])