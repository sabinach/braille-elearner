import pygame
import speech_recognition as sr

def sphinx_api(recognizer, audio):
    # recognize speech using Sphinx
    print("Parsing..")
    try:
        print("Sphinx thinks you said " + recognizer.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def google_api(recognizer, audio):
    # recognize speech using Google Speech Recognition
    print("Parsing..")
    try:
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def speech_to_text(api):
    # obtain audio from the microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

        # select speech recognition api
        if api=="sphinx": sphinx_api(recognizer, audio)
        if api=="google": google_api(recognizer, audio)


def get_keypress():
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
                speech_to_text(api="google")  

    
if __name__ == '__main__':
    # initialize pygame display
    pygame.init()

    # set window size
    pygame.display.set_mode((200,200)) #width, height

    # wait for "return" keypress -> listen to audio
    get_keypress()

    # close pygame
    pygame.quit()

