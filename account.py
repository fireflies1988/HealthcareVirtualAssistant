import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow

import pyrebase

import createacc
import login
import signup_form

firebaseConfig = {'apiKey': "AIzaSyB9O5m92e395fNLlFzqUF7xTmNBtUcxb4c",
                  'authDomain': "nhung-c3e4e.firebaseapp.com",
                  'databaseURL': "https://nhung-c3e4e-default-rtdb.firebaseio.com",
                  'projectId': "nhung-c3e4e",
                  'storageBucket': "nhung-c3e4e.appspot.com",
                  'messagingSenderId': "847152446523",
                  'appId': "1:847152446523:web:db274ff6fc2c6e8ed6f01e",
                  'measurementId': "G-2404E27MXC"}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__()
        self.main_win = QDialog()
        self.uic = login.Ui_Dialog()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.uic.setupUi(self.main_win)
        self.parent = parent
        self.uic.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.createaccbutton.clicked.connect(self.goto_create)
        self.uic.invalid.setVisible(False)
        # dialog = MainWindow()

    def login_function(self):
        email = self.uic.email.text()
        password = self.uic.password.text()
        try:
            ref = auth.sign_in_with_email_and_password(email, password)
            global uid
            uid = ref['localId']
            # mainwindow = MainWindow()
            # widget.addWidget(MainWindow())
            # widget.setCurrentIndex(widget.currentIndex() + 1)
            # self.window = QtWidgets.QMainWindow()
            mainwindow2 = MainWindow()
            mainwindow2.show()
            self.close()
            print(ref['localId'])
            self.parent = self.parent()
            self.parent.show()
        except Exception as e:
            self.uic.invalid.setVisible(True)

    def goto_create(self):
        createAcc = CreateAcc()
        createAcc.show()
        self.close()
        # widget.addWidget(createAcc)
        # widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        self.main_win = QDialog()
        self.uic = createacc.Ui_Dialog()
        self.uic.setupUi(self.main_win)
        self.uic.signupbutton.clicked.connect(self.create_acc_function)
        self.uic.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.uic.invalid.setVisible(False)

    def create_acc_function(self):
        email = self.uic.email.text()
        if self.uic.password.text() == self.uic.confirmpass.text():
            password = self.uic.password.text()
            try:
                auth.create_user_with_email_and_password(email, password)
                login = Login()
                # widget.addWidget(login)
                # widget.setCurrentIndex(widget.currentIndex() + 1)
            except BaseException as e:
                self.uic.invalid.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = Login()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(480)
    widget.setFixedHeight(620)
    widget.show()
    app.exec_()
