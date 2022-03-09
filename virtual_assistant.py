import speech_recognition as sr
from time import ctime
import webbrowser
import playsound
import os
import random
from gtts import gTTS
import pyttsx3

recognizer = sr.Recognizer()


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            voice_data = recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            # speak("Sorry, I did not get that.")
            raise sr.UnknownValueError
        except sr.RequestError:
            # speak("Sorry, my speech service is down.")
            raise sr.RequestError
        return voice_data


def respond(voice_data):
    if "what is your name" in voice_data:
        speak("My name is Zira")
    elif "what time is it" in voice_data:
        speak(ctime())
    elif "search" in voice_data:
        search = record_audio("What do you want to search for?")
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
        speak("Here is what I found for " + search)
    elif "find location" in voice_data:
        location = record_audio("What is the location?")
        url = "https://google.nl/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
        speak("Here is the location of " + location)
    elif "heart rate" in voice_data:
        speak("Please put your finger on the sensor and hold on a moment.")
        # Do something...

    else:
        speak("Sorry, I'm not able to help with this one.")


def speak(audio_string):
    # use gtts
    # tts = gTTS(text=audio_string, lang="en")
    # rand = random.randint(1, 10000000)
    # audio_file = "audio-" + str(rand) + ".mp3"
    # tts.save(audio_file)
    # playsound.playsound(audio_file)
    # print(audio_string)
    # os.remove(audio_file)

    # os.remove(audio_file) is not working so I use pyttsx3 instead
    print(audio_string)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)   # voices[0]: male voice, voices[1]: female voice
    engine.say(audio_string)
    engine.runAndWait()


def introduce():
    playsound.playsound('sound/cortana_sound_effect.mp3')
    speak("Hi, I'm your healthcare virtual assistant. What can I do for you?")