import sys
sys.path.insert(0, '../lib/')

import os
import time
import Leap
import keyboard

import utils
from params import *

# get complete file name
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)

# get min/max x bounds
MIN_X, MAX_X, NUM_CELLS, CELL_LENGTH = utils.get_leap_boundaries(filepath=root_dir+"/json/leap_boundaries.json")


class IndexFinger(Leap.Listener):

    def on_init(self, controller):
        self.HAND_CONFIDENCE_THRESH = HAND_CONFIDENCE_THRESH
        self.TRANSLATION_PROB_THRESH = TRANSLATION_PROB_THRESH
        self.FINGER_HOLD_TIME = FINGER_HOLD_TIME

        self.previous_cell = -1
        self.current_cell = None

        self.previous_time = None
        self.current_time = None

        self.processed = False

        self.current_symbols = utils.load_json(filepath=root_dir+"/json/current_symbols.json") 

        self.counter = 0 


    def on_connect(self, controller):
        print("Connected.")


    def on_frame(self, controller):
        #print("Frame available")
        frame = controller.frame()
        right_hand = list(filter(lambda hand: hand.is_right, frame.hands))

        if frame.hands:

            if self.counter > WARPED_COUNT:
                utils.speak("Please reset your hands, and make sure your right hand is facing downwards.")
                self.counter = 0

            # get right hand
            if right_hand:
                right_hand = right_hand[0]

                # check: facing downwards, hand confidence, translation prob
                if (right_hand.palm_normal[1]>0) and (right_hand.confidence>self.HAND_CONFIDENCE_THRESH) and (right_hand.translation_probability>self.TRANSLATION_PROB_THRESH):

                        self.counter = 0

                        # 1: index finger, 0: only one index finger on right hand
                        index_finger = right_hand.fingers.finger_type(1)[0] 
                        x = index_finger.stabilized_tip_position.x

                        # get current braille cell
                        if x>MIN_X and x<MAX_X:
                            self.current_cell = max(0, 9 - int((x-MIN_X)/CELL_LENGTH))

                            # don't process passing movements
                            if self.processed and self.current_cell==self.previous_cell:
                                self.current_time = time.time()
                                hold_time = self.current_time - self.previous_time
                                if hold_time > self.FINGER_HOLD_TIME:
                                    letter = str(self.current_symbols[self.current_cell])
                                    print("cell: {}, letter: {}".format(self.current_cell, letter))
                                    utils.speak(letter)
                                    self.processed = False

                            # finger moved to new cell
                            elif self.current_cell != self.previous_cell:
                                self.previous_cell = self.current_cell
                                self.previous_time = time.time()
                                self.processed = True

                else:
                    self.counter += 1

            else:
                self.counter += 1


def learn_mode(pygame, key_back, key_exit):

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images
    print("Connecting to Leap..")

    # Listener
    indexFinger = IndexFinger()

    # Have listeners receive events from the controller
    controller.add_listener(indexFinger)

    # Keep this process running until exit is pressed
    while True:
        
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT: 
            break

        # captures the 'KEYDOWN' events
        if event.type == pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)

            # keypress to go back to menu
            if keyname == key_back:
                break

            # keypress to go back to menu
            if keyname == key_exit:
                break

    controller.remove_listener(indexFinger)


if __name__ == "__main__":

    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        learn_intro = "Please move your right finger over each braille cell to hear its symbol name. Keep your hand extended, and make sure the leap motion visualizer recognizes your RIGHT hand. Reset by removing your hand from view if necessary."
        utils.speak(learn_intro)

    #------- Learn Mode -------#

    learn_mode()

