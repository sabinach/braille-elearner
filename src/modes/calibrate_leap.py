import sys
sys.path.insert(0, '../lib/') # for Leap.py

import Leap
from Leap import *


class Pointer(Leap.Listener):

    def on_init(self, controller):
        self.TRANSLATION_PROBABILITY_THRESHOLD = 0.5

    def on_connect(self, controller):
        print("Connected")

    def on_frame(self, controller):
        #print("Frame available")
        frame = controller.frame()
        right_hand = list(filter(lambda hand: hand.is_right, frame.hands))

        # get right hand
        if right_hand:
            right_hand = right_hand[0]

            # facing downwards
            if right_hand.palm_normal[1]>0:

                # estimated probability that the hand motion between the current frame and the specified frame is intended to be a translating motion
                if right_hand.translation_probability > self.TRANSLATION_PROBABILITY_THRESHOLD:

                    # 1: index finger, 0: only one index finger on right hand
                    index_finger = right_hand.fingers.finger_type(1)[0] 
                    x = index_finger.stabilized_tip_position.x
                    print(x)

def main():

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images

    # Listener
    pointer = Pointer()

    # Have listeners receive events from the controller
    controller.add_listener(pointer)

    # Keep this process running until Enter is pressed
    #print("Press LEFT and RIGHT arrows to save leap calibration...")
    print("Press CTRL-C (terminal focus) to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(pointer)

    # Save leap boundaries
    #self.LEAP_BOUNDARIES = utils.load_json(filepath=root_dir+"/json/leap_boundaries.json")
    #utils.save_json(leap_boundaries, filepath=root_dir+"/json/leap_boundaries.json")


if __name__ == "__main__":
    main()