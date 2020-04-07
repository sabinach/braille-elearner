# Parameters
MIN_X = -153 # rightmost
MAX_X = 24  # leftmost
BRAILLE = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9:'j'}

# Constants
NUM_CELLS = 10
CELL_LENGTH = (MAX_X-MIN_X)/(NUM_CELLS)

# Leap Motion
HAND_CONFIDENCE_THRESH = 0.5
TRANSLATION_PROB_THRESH = 0.5
FINGER_HOLD_TIME = 0.8