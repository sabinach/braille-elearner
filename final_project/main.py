import os
import sys
sys.path.insert(0, 'lib/')
import Leap
import string
import time

# Parameters
MIN_X = -146 # rightmost
MAX_X = 24  # leftmost

NUM_CELLS = 10
CELL_LENGTH = (MAX_X-MIN_X)/(NUM_CELLS)

braille_cells = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}


def speak(text):
    table = string.maketrans("","")
    cleaned_text = text.translate(table, string.punctuation) 
    os.system("say '{}'".format(cleaned_text))


class Pointer(Leap.Listener):

    def on_init(self, controller):
        self.HAND_CONFIDENCE_THRESH = 0.5
        self.TRANSLATION_PROB_THRESH = 0.5
        self.FINGER_HOLD_TIME = 0.8

        self.previous_cell = -1
        self.current_cell = None

        self.previous_time = None
        self.current_time = None

        self.processed = False

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
                                print(self.current_cell)
                                speak(str(self.current_cell))
                                self.processed = False

                        elif self.current_cell != self.previous_cell:
                            self.previous_cell = self.current_cell
                            self.previous_time = time.time()
                            self.processed = True


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
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(pointer)


if __name__ == "__main__":
    main()