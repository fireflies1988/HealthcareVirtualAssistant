import sys
import threading

import playsound
from PyQt5.QtWidgets import QMainWindow, QApplication

import account
from main import SpeechRunnable
from signup_form import Ui_MainWindow


class MainWindow:
    def __init__(self):
        self.speechRunnable = None
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        # self.uic.signupbutton.clicked.connect(self.create_acc_function)
        threading.Thread(target=self.introduce2, daemon=True).start()
        # self.uic.password.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.uic.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        # self.uic.invalid.setVisible(False)

    def introduce2(self):
        # self.uic.chat_bot.setText("Hi, I'm your healthcare virtual assistant. \nWhat can I do for you?")
        playsound.playsound('sound/cortana_sound_effect.mp3')
        self.speechRunnable = SpeechRunnable()
        self.speechRunnable.speak("Hi, I'm your healthcare virtual assistant. What can I do for you?")

    def show(self):
        self.main_win.show()

    # def create_acc_function(self):
    #     email = self.uic.email.text()
    #     if self.uic.password.text() == self.uic.confirmpass.text():
    #         user_password = self.uic.password.text()
    #         try:
    #             account.auth.create_user_with_email_and_password(email, user_password)
    #             login = account.Login()
    #             # widget.addWidget(login)
    #             # widget.setCurrentIndex(widget.currentIndex() + 1)
    #         except:
    #             self.uic.invalid.setVisible(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    # login_form = Login()
    # login_form.show()
    # main_win = MainWindow()
    # main_win.show()
    sys.exit(app.exec())
