import os
import string
import speech_recognition as sr

def speak(text):
    table = string.maketrans("","")
    cleaned_text = text.translate(table, string.punctuation) 
    os.system("say '{}'".format(cleaned_text))


def sphinx_api(recognizer, audio):
    # recognize speech using Sphinx
    parsed_audio = None
    try:
        parsed_audio = recognizer.recognize_sphinx(audio)
        print("Sphinx thinks you said: {}".format(parsed_audio))
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
        print("Google Speech Recognition thinks you said: {}".format(parsed_audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return parsed_audio