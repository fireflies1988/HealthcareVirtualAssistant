import sys

import pyttsx3 as pyttsx3
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import Ui_MainWindow
# from virtual_assistant import introduce
from virtual_assistant_2 import *
from alarm_dialog import Ui_Dialog

global command
command = ""


class SpeechRunnable(QRunnable):
    def __init__(self):
        QRunnable.__init__(self)
        self.chat_speech = None
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # voices[0]: male voice, voices[1]: female voice

    def run(self):
        self.engine.say(self.chat_speech)
        self.engine.runAndWait()
        # self.engine.endLoop()  # add this line
        # self.engine.stop()

    def speak(self, text):
        self.chat_speech = text
        QThreadPool.globalInstance().start(self)

    def stop(self):
        self.engine.stop()


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.btn_speak.clicked.connect(self.on_click_speak_button)
        self.uic.btnUpdate.clicked.connect(self.updatePatient)

        self.uic.lineEditPatientCode.setText("patientcode")
        self.uic.lineEditName.setText("name")
        self.uic.radioButtonMale.setChecked(True)

        self.uic.lineEditPhone.setText("0158181858")
        self.uic.textEditDisease.setText("ooooo\naaaaaa")

        self.uic.btn_send.clicked.connect(self.on_click_send)
        self.uic.heart_widget.hide()
        self.uic.weather_widget.hide()
        self.speechRunnable = None
        self.speechRunnable = SpeechRunnable()
        threading.Thread(target=introduce2, args={self}, daemon=True).start()

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
        global command
        global isListening
        if not isListening:
            isListening = not isListening
            # threading.Thread(target=change_speak_button_status).start()
            # change_speak_button_status()
            threading.Thread(target=listen2).start()

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
