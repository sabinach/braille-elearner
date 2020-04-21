import utils
from params import *
import pygame


def cvimage_to_pygame(img):
    """Convert cvimage into a pygame image"""
    return pygame.image.frombuffer(img.tostring(), img.shape[:2], "RGB")


def setup_mode():
    # wait for "return" keypress -> listen to audio
    while True:
        # gets a single event from the event queue
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT: 
            break

        # captures the 'KEYDOWN' events
        if event.type == pygame.KEYDOWN:
            keyname = pygame.key.name(event.key)
            if keyname == "return":
                print("return")

        pygame.display.update()



if __name__ == '__main__':
    #------- Welcome Speech -------#

    # welcome speech (instructions)
    if INTRO:
        setup_intro = "Generating new braille symbols..."
        utils.speak(setup_intro)

    #------- Pygame -------#

    # initialize pygame display
    pygame.init()

    # set window size
    pygame.display.set_caption("OpenCV camera stream on Pygame")
    pygame.display.set_mode([1280,960]) # width, height

    #------- Setup Mode -------#
    setup_mode()

    # close pygame
    pygame.quit()

