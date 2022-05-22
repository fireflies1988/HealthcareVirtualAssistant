import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import *
from app import Ui_MainWindow

global command
command = ""


def hello():
    speak("hello")


def listen2():
    playsound.playsound('sound/data_2.wav')
    global isListening
    global command
    try:
        command = record_audio()
        respond2(command)
        isListening = not isListening
        # speakButton.config(image=blueEdgeMicIcon)
    except sr.UnknownValueError:
        isListening = not isListening
        # speakButton.config(image=blueEdgeMicIcon)
    except sr.RequestError:
        isListening = not isListening
        # speakButton.config(image=blueEdgeMicIcon)


def respond2(voice_data):
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
        weather()

    elif "heart rate" in voice_data:  # display heart rate of user
        arduino_data = sensor.init_sensor()
        if arduino_data is None:
            speak("This function is not available!")
        else:
            speak("Place your index finger on the sensor with steady pressure.")
            # sensor.measure(arduino_data)
            sensor.measure_max30100(arduino_data)

    elif "temperature" in voice_data:
        sensor.read_temperature()
        pass

    elif "where am i" in voice_data:
        my_location()

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

    elif "set alarm" in voice_data:  # set alarm
        time = record_audio("what is the time")

    else:
        speak("Sorry, I'm not able to help with this one.")


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.btn_set_alarm.clicked.connect(hello)
        self.uic.btn_speak.clicked.connect(self.on_click_speak_button)
        self.uic.btnUpdate.clicked.connect(self.updatePatient)

        self.uic.lineEditPatientCode.setText("patientcode")
        self.uic.lineEditName.setText("name")
        self.uic.radioButtonMale.setChecked(True)

        self.uic.lineEditPhone.setText("0158181858")
        self.uic.textEditDisease.setText("ooooo\naaaaaa")

        threading.Thread(target=introduce, daemon=True).start()

    def show(self):
        self.main_win.show()

    def updatePatient(self):
        code = self.uic.lineEditPatientCode.text()
        name = self.uic.lineEditName.text()
        sex = ""
        if self.uic.radioButtonMale.isChecked():
            sex = self.uic.radioButtonMale.text()
        else:
            sex = self.uic.radioButtonFemale.text()
        phone = self.uic.lineEditPhone.text()
        disease = self.uic.textEditDisease.toPlainText()
        print(name+" "+phone+" "+sex+" "+disease)

    def on_click_speak_button(self):
        global command
        global isListening
        if not isListening:
            isListening = not isListening
            # threading.Thread(target=change_speak_button_status).start()
            change_speak_button_status()
            threading.Thread(target=listen2).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

# if __name__ == "__main__":
#     window.after(500, introduce)  # after mainloop() 500ms, call introduce()
#     window.mainloop()
