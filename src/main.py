import pygame
import utils
from params import *

# States
MAIN = 0
USER = 1
SETTINGS = 2
VOLUME = 3
SPEED = 4


main_list = ["user modes", "settings"]
user_list = ["learn mode", "review mode"]
settings_list = ["calibrate leap", "calibrate camera", "volume", "speed"]


def main_menu():

    # overall state
    state = 0

    # internal state
    sub_state = 0

    # flag to signify state change
    new_state = True

    utils.speak("main menu")

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
                    if mode == "learn":
                        print("learn")
                        pass
                    elif mode == "review":
                        print("review")
                        pass
                    utils.speak("selected")

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
                        if mode == "leap":
                            print("leap")
                            pass
                        elif mode == "camera":
                            print("camera")
                            pass
                        utils.speak("selected")

                    elif len(selected) == 1:
                        mode = selected[0]
                        if mode == "volume":
                            state = VOLUME
                            new_state = True
                        elif mode == "speed":
                            state = SPEED
                            new_state = True
                        utils.speak("selected")

                elif keyname == BACK:
                    state = MAIN
                    sub_state = main_list.index("settings")
                    utils.speak("back to main menu")
                    new_state = True

            elif state == VOLUME:
                if keyname == MOVE_BACK:
                    pass
                elif keyname == MOVE_NEXT:
                    pass
                elif keyname == ENTER:
                    state = None
                    sub_state = None

                elif keyname == BACK:
                    state = SETTINGS
                    sub_state = settings_list.index("volume")
                    utils.speak("back to settings")
                    new_state = True

            elif state == SPEED:
                if keyname == MOVE_BACK:
                    pass
                elif keyname == MOVE_NEXT:
                    pass
                elif keyname == ENTER:
                    state = None
                    sub_state = None

                elif keyname == BACK:
                    state = SETTINGS
                    sub_state = settings_list.index("speed")
                    utils.speak("back to settings")
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

