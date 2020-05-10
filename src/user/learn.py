import sys
sys.path.insert(0, '../../lib/')

import os
import time
import Leap

from params import *
import utils

# get complete file name
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent.parent)


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


    def on_connect(self, controller):
        print("Connected")


    def on_frame(self, controller):
        #print("Frame available")
        frame = controller.frame()
        right_hand = list(filter(lambda hand: hand.is_right, frame.hands))

        # get right hand
        if right_hand:
            right_hand = right_hand[0]

            # check: facing downwards, hand confidence, translation prob
            if (right_hand.palm_normal[1]>0) and (right_hand.confidence>self.HAND_CONFIDENCE_THRESH) and (right_hand.translation_probability>self.TRANSLATION_PROB_THRESH):

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


def learn_mode():

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images

    # Listener
    indexFinger = IndexFinger()

    # Have listeners receive events from the controller
    controller.add_listener(indexFinger)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(indexFinger)


if __name__ == "__main__":

    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        learn_intro = "Please move your right finger over each braille cell to hear its symbol name. Keep your hand extended, and make sure the leap motion visualizer recognizes your RIGHT hand. Reset by removing your hand from view if necessary."
        utils.speak(learn_intro)

    #------- Learn Mode -------#

    learn_mode()

