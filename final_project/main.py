import os
import sys
sys.path.insert(0, 'lib/')
import Leap
import string


MIN_X = -146 # rightmost
MAX_X = 25  # leftmost
NUM_CELLS = 10
CELL_LENGTH = (MAX_X-MIN_X)/(NUM_CELLS)

braille_cells = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 6: 'f', 7: 'g', 8: 'h', 9: 'i'}


def speak(text):
    table = string.maketrans("","")
    cleaned_text = text.translate(table, string.punctuation) 
    os.system("say '{}'".format(cleaned_text))


class Pointer(Leap.Listener):

    def on_init(self, controller):
        self.TRANSLATION_PROBABILITY_THRESHOLD = 0.5
        self.previous_cell = -1
        self.current_cell = 0

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

                    # get current braille cell
                    if (x>MIN_X and x<MAX_X):
                        self.current_cell = max(0, 9 - int((x-MIN_X)/CELL_LENGTH))
                        if self.current_cell != self.previous_cell:
                            self.previous_cell = self.current_cell
                            print(self.current_cell)
                            speak(str(self.current_cell))

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