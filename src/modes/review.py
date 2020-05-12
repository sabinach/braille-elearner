import sys
sys.path.insert(0, '../lib/')

import Leap
import pygame
import speech_recognition as sr

import utils
from params import *
import time

# get complete file name
import os
from pathlib import Path
curr_dir = Path(os.getcwd())
root_dir = str(curr_dir.parent)

# Global variables; Do not modify!
audio_input = None
process_speech = False

previous_cell = -1
current_cell = None

# Get current braille symbols loaded in system
current_symbols = utils.load_json(filepath=root_dir+"/json/current_symbols.json") 

# get min/max x bounds
MIN_X, MAX_X, NUM_CELLS, CELL_LENGTH = utils.get_leap_boundaries(filepath=root_dir+"/json/leap_boundaries.json")

# test connection (because not using listener)
connected = True

# counter for detecting warped hands
counter = 0


def get_frame(controller):
    global audio_input, process_speech, previous_cell, current_cell, connected, counter

    # notify user when connected for the first time
    if connected:
        print("Connected.")
        connected = False

    #print("Frame available")
    frame = controller.frame()
    right_hand = list(filter(lambda hand: hand.is_right, frame.hands))

    if frame:

        if counter > WARPED_COUNT:
            utils.speak("Please reset your hands, and make sure your right hand is facing downwards.")
            counter = 0

        # get right hand
        if right_hand:
            right_hand = right_hand[0]

            # check: facing downwards, hand confidence, translation prob
            if (right_hand.palm_normal[1]>0) and (right_hand.confidence>HAND_CONFIDENCE_THRESH) and (right_hand.translation_probability>TRANSLATION_PROB_THRESH):

                # 1: index finger, 0: only one index finger on right hand
                index_finger = right_hand.fingers.finger_type(1)[0] 
                x = index_finger.stabilized_tip_position.x

                # get current braille cell
                if x>MIN_X and x<MAX_X:
                    current_cell = max(0, 9 - int((x-MIN_X)/CELL_LENGTH))

                    # finger moved to new cell
                    if current_cell != previous_cell:
                        previous_cell = current_cell
                        utils.speak("Ready")
                        counter = 0

                    # don't process passing movements
                    elif current_cell==previous_cell:

                        if process_speech:
                            letter = str(current_symbols[current_cell])
                            print("cell: {}, letter: {}".format(current_cell, letter))

                            # convert back to alphabet ie. "why" -> "y"
                            if audio_input in MISHEARD_LETTERS:
                                audio_input = MISHEARD_LETTERS[audio_input]

                            if audio_input == letter:
                                print("Correct!")
                                utils.speak("Correct! This is: {}".format(letter))
                            elif audio_input == "help":
                                print("Help!")
                                utils.speak("This is: {}".format(letter))
                            else:
                                print("Try again!")
                                utils.speak("Try again!")

                            process_speech = False
                            print("")

            else:
                counter += 1

        else:
            counter += 1



def listen(api):
    global audio_input, process_speech

    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        #utils.speak("Listening")
        audio = recognizer.listen(source, timeout=TIMEOUT)
        audio_input = None

        # select speech recognition api
        if api=="sphinx": 
            audio_input = utils.sphinx_api(recognizer, audio)
        if api=="google": 
            audio_input = utils.google_api(recognizer, audio)

        if audio_input is not None:
            audio_input = audio_input.lower()
            process_speech = True


def review_mode(pygame, key_enter, key_back, key_exit):

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    print("Connecting to Leap..")

    # wait for "return" keypress -> listen to audio
    while True:
        # leap motion frames
        get_frame(controller)

        # gets a single event from the event queue
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT: 
            break

        # captures the 'KEYDOWN' events
        if event.type == pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)

            # keypress to guess
            if keyname == key_enter:
                parsed_audio = listen(api=API)

            # keypress to go back to menu
            if keyname == key_back:
                break

            # keypress to go back to menu
            if keyname == key_exit:
                break

        time.sleep(0.1)

    
if __name__ == '__main__':

    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        review_intro = "Please move your right finger over each braille cell. To check the letter of the current cell, press ENTER on the keyboard, and vocalize your guess clearly. To ask for help, press ENTER and say HELP."
        utils.speak(review_intro)

    #------- Pygame -------#

    # initialize pygame display
    #pygame.init()

    # set window size
    #pygame.display.set_mode((200,200)) #width, height

    #------- Leap Motion -------#

    # Controller
    #controller = Leap.Controller()
    #controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images

    #------- Review Mode -------#

    review_mode(controller)

    # close pygame
    #pygame.quit()

