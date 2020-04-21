import sys
sys.path.insert(0, '../lib/')

import os
import Leap
import string
import pygame
import speech_recognition as sr
from params import *
import utils

# Global variables; Do not modify!
audio_input = None
process_speech = False

previous_cell = -1
current_cell = None


def get_frame(controller):
    global audio_input, process_speech, previous_cell, current_cell

    #print("Frame available")
    frame = controller.frame()
    right_hand = list(filter(lambda hand: hand.is_right, frame.hands))

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

                    # don't process passing movements
                    elif current_cell==previous_cell:

                        if process_speech:
                            letter = BRAILLE[current_cell]
                            print("cell: {}, letter: {}".format(current_cell, letter))

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


def review_mode(controller):
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
            if keyname == "return":
                parsed_audio = listen(api=API)

    
if __name__ == '__main__':

    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        review_intro = "Please move your right finger over each braille cell. To check the letter of the current cell, press ENTER on the keyboard, and vocalize your guess clearly. To ask for help, press ENTER and say HELP."
        utils.speak(review_intro)

    #------- Pygame -------#

    # initialize pygame display
    pygame.init()

    # set window size
    pygame.display.set_mode((200,200)) #width, height

    #------- Leap Motion -------#

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images

    #------- Review Mode -------#

    review_mode(controller)

    # close pygame
    pygame.quit()

