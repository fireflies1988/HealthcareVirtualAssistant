# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(480, 620)
        Dialog.setStyleSheet("background-color : rgb(54, 54, 54)")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(180, 50, 111, 71))
        self.label.setStyleSheet("color:  rgb(225, 225, 225); font-size: 28pt;")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(60, 160, 71, 21))
        self.label_2.setStyleSheet("font-size: 15pt; color: rgb(0, 85, 255)")
        self.label_2.setObjectName("label_2")
        self.email = QtWidgets.QLineEdit(Dialog)
        self.email.setGeometry(QtCore.QRect(180, 150, 231, 41))
        self.email.setStyleSheet("font-size: 14pt; color: rgb(243,243,243);")
        self.email.setObjectName("email")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(180, 241, 231, 41))
        self.password.setStyleSheet("font-size: 14pt; color: rgb(243,243,243);")
        self.password.setObjectName("password")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 250, 111, 21))
        self.label_3.setStyleSheet("font-size: 15pt; color: rgb(0, 85, 255)")
        self.label_3.setObjectName("label_3")
        self.loginbutton = QtWidgets.QPushButton(Dialog)
        self.loginbutton.setGeometry(QtCore.QRect(280, 370, 131, 31))
        self.loginbutton.setStyleSheet("background-color: rgb(167, 168, 167);font-size: 14pt; color: rgb(255, 255, 255);")
        self.loginbutton.setObjectName("loginbutton")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(180, 330, 141, 16))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_4.setObjectName("label_4")
        self.createaccbutton = QtWidgets.QPushButton(Dialog)
        self.createaccbutton.setGeometry(QtCore.QRect(320, 320, 93, 28))
        self.createaccbutton.setStyleSheet("color: rgb(255, 255, 255)")
        self.createaccbutton.setObjectName("createaccbutton")
        self.invalid = QtWidgets.QLabel(Dialog)
        self.invalid.setGeometry(QtCore.QRect(180, 290, 231, 20))
        self.invalid.setStyleSheet("font-size: 12pt; color: rgb(255, 0, 0);")
        self.invalid.setObjectName("invalid")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Login"))
        self.label_2.setText(_translate("Dialog", "Email"))
        self.label_3.setText(_translate("Dialog", "Password"))
        self.loginbutton.setText(_translate("Dialog", "Login"))
        self.label_4.setText(_translate("Dialog", "Bạn chưa có tài khoản?"))
        self.createaccbutton.setText(_translate("Dialog", "Create Account"))
        self.invalid.setText(_translate("Dialog", "Invalid email or password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
