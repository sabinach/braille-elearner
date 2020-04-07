import os
import sys
sys.path.insert(0, 'lib/')
import Leap
import string
import time
import pygame
import speech_recognition as sr
from params import *


# Global variables
audio_input = None
process_speech = False

previous_cell = -1
current_cell = None

previous_time = None
current_time = None

processed_time = False


def speak(text):
    table = string.maketrans("","")
    cleaned_text = text.translate(table, string.punctuation) 
    os.system("say '{}'".format(cleaned_text))


def get_frame(controller):
    global audio_input, process_speech, previous_cell, current_cell, previous_time, current_time, processed_time

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
                        previous_time = time.time()
                        processed_time = True

                    # don't process passing movements
                    elif processed_time and current_cell==previous_cell:
                        print("a")
                        current_time = time.time()
                        hold_time = current_time - previous_time

                        if hold_time > FINGER_HOLD_TIME:
                            print("b")

                            if process_speech:
                                print("c")
                                letter = BRAILLE[current_cell]
                                print("cell: {}, letter: {}".format(current_cell, letter))

                                if audio_input == letter:
                                    speak("Correct! This is: {}".format(letter))
                                elif audio_input == "help":
                                    speak("This is: {}".format(letter))
                                else:
                                    speak("Try again!")

                                processed_time = False
                                process_speech = False



def sphinx_api(recognizer, audio):
    # recognize speech using Sphinx
    parsed_audio = None
    try:
        parsed_audio = recognizer.recognize_sphinx(audio)
        print("Sphinx thinks you said " + parsed_audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return parsed_audio


def google_api(recognizer, audio):
    # recognize speech using Google Speech Recognition
    parsed_audio = None
    try:
        parsed_audio = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + parsed_audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return parsed_audio


def listen(api):
    global audio_input, process_speech

    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)
        audio_input = None

        # select speech recognition api
        if api=="sphinx": 
            audio_input = sphinx_api(recognizer, audio)
        if api=="google": 
            audio_input = google_api(recognizer, audio)

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
                parsed_audio = listen(api="google")

    
if __name__ == '__main__':

    # initialize pygame display
    pygame.init()

    # set window size
    pygame.display.set_mode((200,200)) #width, height

    #------- Leap Motion -------#

    # Controller
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_OPTIMIZE_HMD)  # Head-mounted tracking
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)       # Receive images

    #------- Pygame -------#

    review_mode(controller)

    # close pygame
    pygame.quit()

