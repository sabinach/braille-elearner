import sys
sys.path.insert(0, '../lib/') # for Leap.py

import Leap
from Leap import *

import utils
from params import *

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)

x = None

class Pointer(Leap.Listener):

    def on_init(self, controller):
        self.TRANSLATION_PROBABILITY_THRESHOLD = 0.5
        self.counter = 0 

    def on_connect(self, controller):
        print("Connected.")

    def on_frame(self, controller):
        global x

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

                # facing downwards
                if right_hand.palm_normal[1]>0:

                    self.counter = 0

                    # estimated probability that the hand motion between the current frame and the specified frame is intended to be a translating motion
                    if right_hand.translation_probability > self.TRANSLATION_PROBABILITY_THRESHOLD:

                        # 1: index finger, 0: only one index finger on right hand
                        index_finger = right_hand.fingers.finger_type(1)[0] 
                        x = index_finger.stabilized_tip_position.x
                        print(x)

                else:
                    self.counter += 1

            else:
                self.counter += 1


def track_leap(pygame, key_left, key_right, key_enter, key_back, key_shutdown):
    global x

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images
    print("Connecting to Leap..")

    # Listener
    pointer = Pointer()

    # Have listeners receive events from the controller
    controller.add_listener(pointer)

    # Get boundary info
    leap_boundaries = utils.load_json(filepath=root_dir+"/json/leap_boundaries.json")

    # Keep this process running until exit is pressed
    while True:
        
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT: 
            break

        # captures the 'KEYDOWN' events
        if event.type == pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)

            # set leftmost boundary (MAX_X)
            if keyname == key_left:
                leap_boundaries[0]["MAX_X"] = x
                print(leap_boundaries)
                utils.speak("left boundary selected")

            # set rightmost boundary (MIN_X)
            if keyname == key_right:
                leap_boundaries[0]["MIN_X"] = x
                print(leap_boundaries)
                utils.speak("right boundary selected")

            # save boundaries into json
            if keyname == key_enter:
                min_x = leap_boundaries[0]["MIN_X"]
                max_x = leap_boundaries[0]["MAX_X"]
                num_cells = leap_boundaries[0]["NUM_CELLS"]
                leap_boundaries[0]["CELL_LENGTH"] = (max_x-min_x)/num_cells
                utils.save_json(leap_boundaries, savepath=root_dir+"/json/leap_boundaries.json")

                print(leap_boundaries)
                utils.speak("saved leap calibration")

            # keypress to go back to menu
            if keyname == key_back:
                break

            # keypress to go back to menu
            if keyname == key_shutdown:
                break


    controller.remove_listener(pointer)


if __name__ == "__main__":
    track_leap()