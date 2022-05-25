import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

import ReadWriteKey
import signin_form
import signup_form
from app import Ui_MainWindow
from main import main


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # the way app working
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.thread = {}
        self.alarm_thread = {}
        self.uic.setupUi(self.main_win)
        self.is_btn_speak_clicked = False
        self.is_speaking = False


class SignInForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.uic = signin_form.Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.loginbutton.clicked.connect(self.login_function)
        self.uic.createaccbutton.clicked.connect(self.goto_create)
        self.uic.invalid.setVisible(False)

    def login_function(self):
        global email
        global user_password
        email = self.uic.email.text()
        user_password = self.uic.password.text()
        try:
            # ref = account.auth.sign_in_with_email_and_password(email, user_password)
            # print(ref['localId'])
            mainWindow = MainWindow()
            mainWindow.show()
            self.main_win.close()
            # ReadWriteKey.writeFile(key=ref['localId'])

        except Exception as e:
            self.uic.invalid.setVisible(True)

    def goto_create(self):
        print("tsign up")
        signUpForm = SignInForm()
        signUpForm.show()
        # self.showSignUpForm()

    def showSignUpForm(self):
        self.sub_win = QMainWindow()
        self.uic1 = signup_form.Ui_MainWindow()
        self.uic1.setupUi(self)
        self.sub_win.show()

    def show(self):
        self.main_win.show()


class SignUpForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.uic = signup_form.Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.uic.signupbutton.clicked.connect(self.create_acc_function)
        self.uic.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.btnback.clicked.connect(self.goto_signin)
        self.uic.invalid.setVisible(False)

    def goto_signin(self):
        print("sign in")
        self.showSignInForm()

    def create_acc_function(self):
        email = self.uic.email.text()
        if self.uic.password.text() == self.uic.confirmpass.text():
            user_password = self.uic.password.text()
            try:
                # account.auth.create_user_with_email_and_password(email, user_password)
                self.showSignInForm()
                # widget.addWidget(login)
                # widget.setCurrentIndex(widget.currentIndex() + 1)
            except:
                self.uic.invalid.setVisible(True)

    def showSignInForm(self):
        self.main_win.close()
        self.sub_win = QMainWindow()
        self.uic1 = signin_form.Ui_MainWindow()
        self.uic1.setupUi(self.sub_win)
        self.sub_win.show()

    def show(self):
        self.main_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    access = ReadWriteKey.checkFile()
    main_win = None
    if access:
        main_win = MainWindow()
    else:
        main_win = SignInForm()
    main_win.show()
    sys.exit(app.exec())
    # app = QApplication([SignInForm, SignUpForm, MainWindow])
    # gui = SignInForm()
    # gui.show()
    # app.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    access = ReadWriteKey.checkFile()
    main_win = None
    if access:
        main_win = MainWindow()
    else:
        main_win = SignInForm()
    # main_win = MainWindow()
    # main_win.show()
    main_win.show()
    sys.exit(app.exec())
    # app = QApplication([SignInForm, SignUpForm, MainWindow])
    # gui = SignInForm()
    # gui.show()
    # app.exec_()
