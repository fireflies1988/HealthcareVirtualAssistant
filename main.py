import sys
import time

import pyttsx3 as pyttsx3
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from SensorData import SensorData
from app import Ui_MainWindow
# from virtual_assistant import introduce
from sensor import read_sensor
from virtual_assistant import speak
from virtual_assistant_2 import *
from alarm_dialog import Ui_Dialog
import speech_recognition as sr

global command
command = ""


class SpeechRunnable(QRunnable):
    def __init__(self):
        super().__init__()
        self.chat_speech = None
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # voices[0]: male voice, voices[1]: female voice

    def run(self):
        self.engine.say(self.chat_speech)
        self.engine.runAndWait()

        if self.engine._inLoop:
            self.engine.endLoop()

    # self.engine.endLoop()  # add this line
    # self.engine.stop()

    def speak(self, text):
        self.chat_speech = text
        QThreadPool.globalInstance().start(self)

    def stop(self):
        self.engine.stop()


class ThreadClass(QThread):
    signal = pyqtSignal(str)

    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        print('Starting thread...', self.index)
        counter = 0
        while True:
            counter += 1
            print(counter)
            if counter == 10:
                counter = 0
            self.signal.emit(str(counter))
            time.sleep(1)

    def stop(self):
        print('Stopping thread', self.index)
        self.terminate()


class ThreadClass2(QThread):
    error_signal = pyqtSignal(str)
    measuring_signal = pyqtSignal(str)
    heart_rate_signal = pyqtSignal(str)
    spo2_signal = pyqtSignal(str)

    def __init__(self, index=0, arduino_data=None):
        super().__init__()
        self.index = index
        self.arduino_data = arduino_data

    def run(self):
        raw_data = []
        flag = True
        timeout = None
        count = 0

        while flag:
            data_from_sensor = read_sensor(self.arduino_data)
            print(data_from_sensor)
            data = data_from_sensor.split(",")
            if data.__len__() > 1:  # chỉ lấy dữ liệu có đầy đủ cả hai phần tử
                if data[0] == "0" or data[1] == "0":
                    timeout = None
                    raw_data.clear()
                    count += 1

                    if count > 5:
                        self.error_signal.emit("Place your index finger on the sensor")
                        count = 0
                    continue

                if timeout is None:
                    timeout = time.time() + 5

                if time.time() > timeout:
                    flag = False

                else:  # khi mọi thứ đã hoàn hảo
                    sensor_data = SensorData(heart_rate=data[0], spo2=data[1])
                    raw_data.append(sensor_data)
                    self.measuring_signal.emit("Measuring")

            time.sleep(1)

        # tính toán nhịp tim trung bình
        sum_heart_rate = 0
        for d in raw_data:
            sum_heart_rate += int(d.heart_rate)

        avg_heart_rate = int(sum_heart_rate / raw_data.__len__())

        self.heart_rate_signal.emit(f"Your average heart rate is {avg_heart_rate} bpm")
        self.spo2_signal.emit(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")

    def stop(self):
        print('Stopping thread', self.index)
        self.arduino_data.close()
        self.terminate()


class ThreadClass3(QThread):
    voice_data_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, index=0, ask=None):
        super().__init__()
        self.index = index
        self.ask = ask

    def run(self):
        with sr.Microphone() as source:
            if self.ask:
                speak(self.ask)
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)  # lúc đang nghe thì tất cả các luồng sẽ dừng
            try:
                voice_data = recognizer.recognize_google(audio, language="en-US")
                self.voice_data_signal.emit(voice_data)
            except sr.UnknownValueError:
                speak("Sorry, I did not get that.")
                self.error_signal.emit("Sorry, I did not get that.")
                # raise sr.UnknownValueError
            except sr.RequestError:
                speak("Sorry, my speech service is down.")
                self.error_signal.emit("Sorry, my speech service is down.")
                # raise sr.RequestError

    def stop(self):
        print('Stopping thread', self.index)
        self.terminate()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # the way app working
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.thread = {}
        self.uic.setupUi(self.main_win)
        self.uic.btn_speak.clicked.connect(self.on_click_speak_button)
        self.uic.btnUpdate.clicked.connect(self.updatePatient)

        self.uic.lineEditPatientCode.setText("patientcode")
        self.uic.lineEditName.setText("name")
        self.uic.radioButtonMale.setChecked(True)

        self.uic.lineEditPhone.setText("0158181858")
        self.uic.textEditDisease.setText("ooooo\naaaaaa")

        self.uic.btn_active.hide()
        self.uic.screen.hide()
        self.uic.btn_send.clicked.connect(self.on_click_send)
        self.uic.heart_widget.hide()
        self.uic.weather_widget.hide()
        self.speechRunnable = SpeechRunnable()

        self.uic.btn_active.clicked.connect(self.start_worker_2)
        threading.Thread(target=introduce2, args={self}, daemon=True).start()

    def start_worker_2(self):
        self.uic.chat_user_widget.hide()
        self.uic.chat_bot_widget.hide()
        self.uic.heart_widget.show()
        self.uic.spo2_label.hide()

        self.speechRunnable = SpeechRunnable()
        arduino_data = sensor.init_sensor()
        if arduino_data is None:
            self.uic.heart_widget.setEnabled(False)
            self.uic.heart_rate_label.setText("This function is not available!")
            self.speechRunnable.speak("This function is not available!")
        else:
            self.uic.heart_rate_label.setText("Place your index finger on the sensor with steady pressure.")
            self.speechRunnable.speak("Place your index finger on the sensor with steady pressure.")
            self.thread[2] = ThreadClass2(index=1, arduino_data=arduino_data)
            self.thread[2].start()
            self.thread[2].error_signal.connect(self.errorWhileMeasuring)
            self.thread[2].measuring_signal.connect(self.measuring)
            self.thread[2].heart_rate_signal.connect(self.showHeartRate)
            self.thread[2].spo2_signal.connect(self.showSpo2)

    def errorWhileMeasuring(self, error_signal):
        self.uic.heart_widget.setEnabled(False)
        self.uic.heart_rate_label.show()
        self.uic.heart_rate_label.setText(error_signal)
        self.speechRunnable = SpeechRunnable()
        self.speechRunnable.speak(error_signal)

    def measuring(self, measuring_signal):
        self.uic.heart_widget.setEnabled(True)
        self.uic.heart_rate_label.show()
        self.uic.heart_rate_label.setText(measuring_signal)
        self.speechRunnable = SpeechRunnable()

    def showHeartRate(self, heart_rate_signal):
        self.uic.heart_widget.setEnabled(True)
        self.uic.heart_rate_label.show()
        self.uic.heart_rate_label.setText(heart_rate_signal)
        self.uic.screen.setText(heart_rate_signal)
        speak(heart_rate_signal)

    def showSpo2(self, spo2_signal):
        self.uic.heart_widget.setEnabled(True)
        self.uic.spo2_label.show()
        self.uic.spo2_label.setText(spo2_signal)
        self.uic.screen.setText(spo2_signal)
        speak(spo2_signal)
        self.thread[2].stop()

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
        print(name + " " + phone + " " + sex + " " + disease)

    def on_click_speak_button(self):
        # global command
        # global isListening
        # isListening = False
        # if not isListening:
        #     isListening = not isListening
        # threading.Thread(target=change_speak_button_status).start()
        # change_speak_button_status()
        self.speechRunnable = SpeechRunnable()
        self.thread[3] = ThreadClass3(index=1)
        self.thread[3].start()
        self.thread[3].voice_data_signal.connect(self.updateUI)
        self.thread[3].error_signal.connect(self.errorWhileHearing)

        # threading.Thread(target=listen2(self)).start()

    def updateUI(self, voice_data_signal):
        self.uic.chat_user.setText(voice_data_signal)
        respond2(self, voice_data_signal)
        # speak(voice_data_signal)

    def errorWhileHearing(self, error_signal):
        self.uic.chat_user.setText("...")
        self.uic.chat_bot.setText(error_signal)

    def on_click_send(self):
        text = ""
        self.speechRunnable = SpeechRunnable()
        if self.uic.ask_entry.text() != "":
            text = self.uic.ask_entry.text()
            self.uic.chat_user.setText(text)
            self.uic.ask_entry.setText("")
            # self.speechRunnable.speak(text)
            respond2(self, text)
            # print(text)

        # threading.Thread(target=respond2(self, text), daemon=True).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

# if __name__ == "__main__":
#     window.after(500, introduce)  # after mainloop() 500ms, call introduce()
#     window.mainloop()
