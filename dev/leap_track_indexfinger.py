import sys
sys.path.insert(0, '../lib/')
import Leap
from Leap import *

class IndexFinger(Leap.Listener):

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
    main()