import speech_recognition as sr
import webbrowser
import playsound
import os
import random
from gtts import gTTS
import pyttsx3
from datetime import datetime
import sensor
from requests_html import HTMLSession
import requests
import pyjokes

recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voices[0]: male voice, voices[1]: female voice


def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)  # lúc đang nghe thì tất cả các luồng sẽ dừng
        try:
            voice_data = recognizer.recognize_google(audio, language="en-US")
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
            raise sr.UnknownValueError
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            raise sr.RequestError
        return voice_data


def respond(voice_data):
    voice_data = voice_data.lower()
    print(voice_data)
    if "what is your name" in voice_data or "your name" in voice_data:
        speak("My name is Zira")
    elif "what time is it" in voice_data or "what is the time" in voice_data:
        speak(datetime.now().strftime('%H:%M'))
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

    elif "weather" in voice_data:
        weather_scrapping()

    elif "heart rate" in voice_data:  # display heart rate of user
        arduino_data = sensor.init_sensor()
        if arduino_data is None:
            speak("This function is not available!")
        else:
            speak("Place your index finger on the sensor with steady pressure.")
            sensor.measure(arduino_data)

    elif "bmi" in voice_data:  # calculate BMI index
        h = record_audio("Please tell me your height")
        w = record_audio("Please tell me your weight")
        height = float(h)
        weight = float(w)
        bmi(height, weight)

    elif "hospital" in voice_data:  # search for hospital nearby
        url = "https://google.com/search?q=hospital-near-me"
        webbrowser.get().open(url)
        speak("I found a few hospitals near you.")

    elif "joke" in voice_data:  # tell s stupid joke
        my_joke = pyjokes.get_joke(language='en', category='all')
        speak(my_joke)

    else:
        speak("Sorry, I'm not able to help with this one.")


def covid_track():
    speak("total case in vietnam is 19000")


def my_location():
    speak('My location is 1029')


def weather_scrapping():
    s = HTMLSession()
    query = 'ho chi minh city'
    url = f'https://www.google.com/search?q=weather+{query}'

    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'})

    temp = r.html.find('span#wob_tm', first=True).text
    unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
    desc = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text
    speak("The temperature today is" + temp + "degree celsius")


def weather():
    speak("Hello")


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
    engine.say(audio_string)
    engine.runAndWait()


def introduce():
    playsound.playsound('sound/cortana_sound_effect.mp3')
    speak("Hi, I'm your healthcare virtual assistant. What can I do for you?")


def bmi(height, weight):
    result = weight / (height * height)
    if result < 16:
        speak('You are Severe thinness')
    elif result >= 16 & result < 17:
        speak('You are moderate thinness ')
    elif result >= 17 & result < 18.5:
        speak('You are thin')
    elif result >= 18.5 & result < 25:
        speak('You are normal')
    elif result >= 25 & result < 30:
        speak('You are overweight')
    elif result >= 30 & result < 35:
        speak('You are Obese type 1')
    elif result >= 35 & result < 40:
        speak('You are Obese type 2')
    else:
        speak('You are Obese type 3')
