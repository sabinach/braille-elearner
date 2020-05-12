###----- Leap Motion -----###

#MIN_X = -106 # rightmost
#MAX_X = 58 # leftmost

# Constants
#NUM_CELLS = 10
#CELL_LENGTH = (MAX_X-MIN_X)/(NUM_CELLS)

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
VIDEO_PORT = 0

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

# Dot boundary calibration (debugging -- calibrate_camera.py)
PEG_COLORS = {0: (53, 211, 81), 1: (13, 23, 143), 2: (69, 121, 215), 3: (165, 78, 248), 4: (83, 207, 204), 5: (185, 240, 217), 6: (136, 220, 14)}

###----- Keypresses -----###

ENTER = "space"
BACK = "backspace"
MOVE_BACK = "left"
MOVE_NEXT = "right"
#SCROLL_UP = "up"
#SCROLL_DOWN = "down"
EXIT = "escape"

###----- GUI -----###

VOLUME_STEPSIZE = 4
SPEED_STEPSIZE = 50
INITIAL_SPEED = 450 	  # 200
INITIAL_VERBOSITY = False # True: include instructions, False: forego instructions
INITIAL_IMAGE = False     # True: visual, False: blind

# Bundle identifiers: osascript -e 'id of app "Name of App"'
#ITERM_ID = "com.googlecode.iterm2"
#SUBLIME_ID = "com.sublimetext.3"
#PYGAME_ID = "TBD"

