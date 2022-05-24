import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from main import MainWindow

import pyrebase

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
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.invalid.setVisible(False)
        # dialog = MainWindow()
        # dialog.exec_()

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()
        try:
            ref = auth.sign_in_with_email_and_password(email, password)
            print(ref['localId'])
            # mainwindow = MainWindow()
            # widget.addWidget(MainWindow())
            # widget.setCurrentIndex(widget.currentIndex() + 1)
            # self.window = QtWidgets.QMainWindow()
            mainwindow2 = MainWindow()
            mainwindow2.show()
            # self.close()



        except:
            self.invalid.setVisible(True)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.invalid.setVisible(False)

    def createaccfunction(self):
        email = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            try:
                auth.create_user_with_email_and_password(email, password)
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            except:
                self.invalid.setVisible(True)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()
