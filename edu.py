#!/usr/bin/env python

"""
use chatGPT to educate kids
I want to wrap chatGPT for kids education. python programming.
    input: voice to text.
    output: text, and voice.
show me codes:
"""

import speech_recognition as sr
import pyttsx3

# Initialize the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Define a function to listen to speech and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=15)
        if not audio:
            return None
    try:
        print('to recognize_bing')
        text = r.recognize_bing(audio)
        # text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't understand.")
        return None
    except sr.RequestError as e:
        print("Error: " + str(e))
        return None


# Define a function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Main loop to listen to speech and respond
while True:
    # Listen for speech
    text = listen()
    # If speech was detected, process it and respond
    if text:
        response = "I heard you say " + text
        print(response)
        speak(response)
