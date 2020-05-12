# Main file (this was written extremely hastily and messily, will clean up code in the future..)

import sys
sys.path.insert(0, 'modes/')

# libraries
import pygame
import utils
from params import *

# Modes
import calibrate_camera
import calibrate_leap
import learn
import review
import generate_dots

# States
MAIN = 0
USER = 1
SETTINGS = 2
VOLUME = 3
SPEED = 4
VERBOSITY = 5
IMAGES = 6
GENERATE_LEARN = 7
GENERATE_REVIEW = 8
LEARN_MODE = 9
REVIEW_MODE = 10 

# states and sub_states
main_list = ["user modes", "settings"]
user_list = ["learn mode", "review mode"]
settings_list = ["calibrate leap", "calibrate camera", "volume", "speed", "verbosity", "images"]

# initial settings
volume_level = utils.get_current_volume()
speed_level = utils.set_speed(INITIAL_SPEED)
verbose_level = INITIAL_VERBOSITY
image_level = INITIAL_IMAGE
generate_new = True


def main_menu():
    global verbose_level, volume_level, verbose_level, image_level, generate_new

    # overall state
    state = 0

    # internal state
    sub_state = 0

    # flag to signify state change
    new_state = True

    # initial startup
    utils.speak("main menu")

    # initial prompt
    print("Press ESC to exit Braille E-Learner.")


    while True:

        # gets a single event from the event queue
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT: 
            break

        # signify state change
        if new_state:
            if state == MAIN:
                utils.speak(main_list[sub_state])
            elif state == USER:
                utils.speak(user_list[sub_state])
            elif state == SETTINGS:
                utils.speak(settings_list[sub_state])
            elif state == VOLUME:
                pass
            elif state == SPEED:
                pass
            new_state = False

        # captures the 'KEYDOWN' events
        if event.type == pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)
            if keyname == EXIT:
                utils.speak("Goodbye")
                break
            
            if state == MAIN:

                if keyname == MOVE_BACK:
                    sub_state -= 1
                    if sub_state == -1:
                        sub_state = len(main_list) - 1
                    utils.speak(main_list[sub_state])

                elif keyname == MOVE_NEXT:
                    sub_state += 1
                    if sub_state == len(main_list):
                        sub_state = 0
                    utils.speak(main_list[sub_state])

                elif keyname == ENTER:
                    state = sub_state + 1
                    sub_state = 0
                    utils.speak("selected")
                    new_state = True  

                elif keyname == BACK:
                    state = MAIN
                    sub_state = main_list.index(main_list[sub_state])
                    utils.speak("back to main menu")
                    new_state = True 
                    

            elif state == USER:
                if keyname == MOVE_BACK:
                    sub_state -= 1
                    if sub_state == -1:
                        sub_state = len(user_list) - 1
                    utils.speak(user_list[sub_state])

                elif keyname == MOVE_NEXT:
                    sub_state += 1
                    if sub_state == len(user_list):
                        sub_state = 0
                    utils.speak(user_list[sub_state])

                elif keyname == ENTER:
                    mode = user_list[sub_state].split()[0]
                    sub_state = 0
                    utils.speak("selected")

                    # LEARN MODE
                    if mode == "learn":
                        # go back to settings
                        state = GENERATE_LEARN
                        new_state = True
                        print("Generate new dots?.. Press LEFT/RIGHT to toggle choice, SPACE to enter, and DELETE to exit.")
                        utils.speak("Do you want to generate new dots?")
                        if verbose_level:
                            utils.speak("Press the LEFT and RIGHT arrows to toggle choice. Press SPACE to enter, and DELETE to exit.")
                        utils.speak("Current choice is: {}".format(generate_new))


                    # REVIEW MODE
                    elif mode == "review":
                        print("Starting review mode.. Press SPACE to guess, and DELETE to exit.")
                        utils.speak("Starting review mode.")
                        if verbose_level:
                            utils.speak("Move your finger over the braille cells. Press SPACE to verbalize your guess, and DELETE to exit.")
                        review.review_mode(pygame, key_enter=ENTER, key_back=BACK, key_exit=EXIT)
                        utils.speak("exiting review mode")

                        # go back to settings
                        state = USER
                        sub_state = user_list.index("review mode")
                        utils.speak("back to user modes")
                        new_state = True
                    

                elif keyname == BACK:
                    state = MAIN
                    sub_state = main_list.index("user modes")
                    utils.speak("back to main menu")
                    new_state = True
               
            
            elif state == SETTINGS:
                if keyname == MOVE_BACK:
                    sub_state -= 1
                    if sub_state == -1:
                        sub_state = len(settings_list) - 1
                    utils.speak(settings_list[sub_state])

                elif keyname == MOVE_NEXT:
                    sub_state += 1
                    if sub_state == len(settings_list):
                        sub_state = 0
                    utils.speak(settings_list[sub_state])

                elif keyname == ENTER:
                    selected = settings_list[sub_state].split()
                    sub_state = 0

                    # calibration
                    if len(selected) > 1:
                        mode = selected[1]
                        utils.speak("selected")

                        # CALIBRATE LEAP
                        if mode == "leap":
                            print("Calibrating leap.. Press LEFT/RIGHT to set boundaries, SPACE to save, DELETE to exit.")
                            utils.speak("Calibrating leap")
                            if verbose_level:
                                utils.speak("Press the LEFT and RIGHT arrows to set boundaries. Press SPACE to save calibration, and DELETE to exit.")
                            calibrate_leap.track_leap(pygame, key_left=MOVE_BACK, key_right=MOVE_NEXT, key_enter=ENTER, key_back=BACK, key_shutdown=EXIT)

                            # go back to settings
                            state = SETTINGS
                            sub_state = settings_list.index("calibrate leap")
                            utils.speak("back to settings")
                            new_state = True

                        # CALIBRATE CAMERA
                        elif mode == "camera":
                            print("Calibrating camera.. Press SPACE to save, and DELETE to exit.")
                            print("\tMake sure all the dots are pushed up!")
                            utils.speak("Calibrating camera")
                            if verbose_level:
                                utils.speak("Make sure all the dots are pushed up. Press SPACE to save calibration, and DELETE to exit.")
                            calibrate_camera.get_video()
                            utils.speak("Camera calibration saved")

                            # go back to settings
                            state = SETTINGS
                            sub_state = settings_list.index("calibrate camera")
                            utils.speak("back to settings")
                            new_state = True

                    elif len(selected) == 1:
                        mode = selected[0]
                        if mode == "volume":
                            state = VOLUME
                            new_state = True
                            utils.speak("selected")
                            print("Volume settings.. Press LEFT/RIGHT to change volume, and DELETE to exit.")
                            if verbose_level:
                                utils.speak("Press the LEFT and RIGHT arrows to change the volume. Press DELETE to exit.")
                            utils.speak("Current volume is: {}".format(volume_level))

                        elif mode == "speed":
                            state = SPEED
                            new_state = True
                            utils.speak("selected")
                            print("Speed settings.. Press LEFT/RIGHT to edit speech speed, and DELETE to exit.")
                            if verbose_level:
                                utils.speak("Press the LEFT and RIGHT arrows to change the speech speed. Press DELETE to exit.")
                            utils.speak("Current speed is: {}".format(utils.get_current_speed()))

                        elif mode == "verbosity":
                            state = VERBOSITY
                            new_state = True
                            utils.speak("selected")
                            print("Verbosity level.. Press LEFT/RIGHT to toggle verbosity, and DELETE to exit.")
                            if verbose_level:
                                utils.speak("Press the LEFT and RIGHT arrows to toggle verbosity. Press DELETE to exit.")
                            utils.speak("Current verbosity is: {}".format(verbose_level))

                        elif mode == "images":
                            state = IMAGES
                            new_state = True
                            utils.speak("selected")
                            print("Image settings.. Press LEFT/RIGHT to toggle image availability for peg slate set up, and DELETE to exit.")
                            if verbose_level:
                                utils.speak("Press the LEFT and RIGHT arrows to toggle image availability for peg slate set up. Press DELETE to exit.")
                            utils.speak("Current image settings is: {}".format(image_level))

                elif keyname == BACK:
                    state = MAIN
                    sub_state = main_list.index("settings")
                    utils.speak("back to main menu")
                    new_state = True


            elif state == VOLUME:
                if keyname == MOVE_BACK:
                    volume_level -= VOLUME_STEPSIZE
                    utils.set_volume(volume_level)
                    utils.speak(str(volume_level))

                elif keyname == MOVE_NEXT:
                    volume_level += VOLUME_STEPSIZE
                    utils.set_volume(volume_level)
                    utils.speak(str(volume_level))

                elif keyname == BACK:
                    state = SETTINGS
                    sub_state = settings_list.index("volume")
                    utils.speak("back to settings")
                    new_state = True

            elif state == SPEED:
                if keyname == MOVE_BACK:
                    speed_level = utils.get_current_speed()
                    speed_level -= SPEED_STEPSIZE
                    utils.set_speed(speed_level)
                    utils.speak(str(speed_level))

                elif keyname == MOVE_NEXT:
                    speed_level = utils.get_current_speed()
                    speed_level += SPEED_STEPSIZE
                    utils.set_speed(speed_level)
                    utils.speak(str(speed_level))

                elif keyname == BACK:
                    state = SETTINGS
                    sub_state = settings_list.index("speed")
                    utils.speak("back to settings")
                    new_state = True

            elif state == VERBOSITY:
                if (keyname == MOVE_BACK) or (keyname == MOVE_NEXT):
                    verbose_level = not verbose_level
                    utils.speak(str(verbose_level))

                elif keyname == BACK:
                    state = SETTINGS
                    sub_state = settings_list.index("verbosity")
                    utils.speak("back to settings")
                    new_state = True

            elif state == IMAGES:
                if (keyname == MOVE_BACK) or (keyname == MOVE_NEXT):
                    image_level = not image_level
                    utils.speak(str(image_level))

                elif keyname == BACK:
                    state = SETTINGS
                    sub_state = settings_list.index("images")
                    utils.speak("back to settings")
                    new_state = True


            elif state == GENERATE_LEARN:
                if (keyname == MOVE_BACK) or (keyname == MOVE_NEXT):
                    generate_new = not generate_new
                    utils.speak(str(generate_new))

                elif keyname == BACK:
                    # go back to settings
                    state = USER
                    sub_state = user_list.index("learn mode")
                    utils.speak("back to user modes")
                    new_state = True

                elif keyname == ENTER:
                    state = LEARN_MODE
                    new_state = True
                    utils.speak("selected")
                    
                    if generate_new:
                        print("Generating new dots. Match the symbols... Press LEFT/RIGHT to move between cells, SPACE to hear dot numbers, and DELETE to exit.")
                        utils.speak("Please match the generated symbols.")
                        if verbose_level:
                            utils.speak("Match the symbols shown in the image by pushing up the pegs from the bottom of the peg slate. Press the LEFT and RIGHT arrows to move between cells. Press SPACE to hear dot numbers. Press DELETE to exit")
                            if image_level:
                                utils.speak("When cells match, their box will turn green.")
                        all_match = generate_dots.setup_mode()

                        if all_match:
                            utils.speak("Completed setup")

                            print("Starting learn mode.. Press DELETE to exit.")
                            utils.speak("Starting learn mode.")
                            if verbose_level:
                                utils.speak("Move your finger over the braille cells to hear the symbol name. Press DELETE to exit.")
                            learn.learn_mode(pygame, key_back=BACK, key_exit=EXIT)
                            utils.speak("exiting learn mode")

                        else:
                            # go back to settings
                            state = USER
                            sub_state = user_list.index("learn mode")
                            utils.speak("back to user modes")
                            new_state = True

                    else:
                        print("Starting learn mode.. Press DELETE to exit.")
                        utils.speak("Starting learn mode.")
                        if verbose_level:
                            utils.speak("Move your finger over the braille cells to hear the symbol name.  Press DELETE to exit.")
                        learn.learn_mode(pygame, key_back=BACK, key_exit=EXIT)
                        utils.speak("exiting learn mode")

                        # go back to settings
                        state = USER
                        sub_state = user_list.index("learn mode")
                        utils.speak("back to user modes")
                        new_state = True
                




if __name__ == '__main__':

    #------- Welcome Speech -------#

    welcome = "Welcome to Braille E-Learner!"
    utils.speak(welcome)

    #------- Pygame -------#

    # initialize pygame display
    pygame.init()

    # set window size
    pygame.display.set_mode((200,200)) #width, height

    # main menu
    main_menu()

    # close pygame
    pygame.quit()

