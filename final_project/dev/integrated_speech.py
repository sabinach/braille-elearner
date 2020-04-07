import os
import string
import pygame
import speech_recognition as sr


def speak(text):
    table = string.maketrans("","")
    cleaned_text = text.translate(table, string.punctuation) 
    os.system("say '{}'".format(cleaned_text))


def sphinx_api(recognizer, audio):
    # recognize speech using Sphinx
    try:
        parsed_audio = recognizer.recognize_sphinx(audio)
        print("Sphinx thinks you said: ".format(parsed_audio))
        speak("You said {}".format(parsed_audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))


def google_api(recognizer, audio):
    # recognize speech using Google Speech Recognition
    try:
        parsed_audio = recognizer.recognize_google(audio)
        print("Google Speech Recognition thinks you said: ".format(parsed_audio))
        speak("You said {}".format(parsed_audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def listen(api):
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
                listen(api="sphinx") 

    
if __name__ == '__main__':
    # initialize pygame display
    pygame.init()

    # set window size
    pygame.display.set_mode((200,200)) #width, height

    # wait for "return" keypress -> listen to audio
    get_keypress()

    # close pygame
    pygame.quit()

