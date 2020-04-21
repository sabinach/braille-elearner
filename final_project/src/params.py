import sys
sys.path.insert(0, '..')

###----- Leap Motion -----###

# Parameters
MIN_X = -106 # rightmost
MAX_X = 68  # leftmost
BRAILLE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9:'j'}

# Constants
NUM_CELLS = 10
CELL_LENGTH = (MAX_X-MIN_X)/(NUM_CELLS)

# Leap Motion
HAND_CONFIDENCE_THRESH = 0.3	# decimal probability
TRANSLATION_PROB_THRESH = 0.3   # decimal probability
FINGER_HOLD_TIME = 0.8 			# sec

# Testing
INTRO = False					# welcome speech

# Listening
TIMEOUT = 7						# sec
API="google"					# google/sphinx

###----- Camera -----###

# Camera
VIDEO_PORT = 1

# Peg pushed threshold
PEG_THRESHOLD = 200

# Only show braille cells
CROP_WIDTH=550
CROP_HEIGHT=350

# BGR
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Dot boundary calibration (debugging)
SHOW_PEG_CONTOURS = True
SHOW_CELL_DIVIDERS = True
SHOW_CENTER = True
SHOW_PEG_BOUNDS = True
