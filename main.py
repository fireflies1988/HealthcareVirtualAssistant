import speech_recognition as sr
from time import ctime
import webbrowser
import playsound
import os
import random
from gtts import gTTS
from ui import *


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return voice_data


def respond(voice_data):
    if "what is your name" in voice_data:
        speak("My name is Alexa")
    if "what time is it" in voice_data:
        speak(ctime())
    if "search" in voice_data:
        search = record_audio("What do you want to search for?")
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
        speak("Here is what I found for " + search)
    if "find location" in voice_data:
        location = record_audio("What is the location?")
        url = "https://google.nl/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
        speak("Here is the location of " + location)
    if "exit" in voice_data:
        exit()


def speak(audio_string):
    tts = gTTS(text=audio_string, lang="en")
    rand = random.randint(1, 10000000)
    audio_file = "audio-" + str(rand) + ".mp3"
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


r = sr.Recognizer()
window.mainloop()


# speak("Hi, say something...")
# while 1:
#     data = record_audio()
#     respond(data)
