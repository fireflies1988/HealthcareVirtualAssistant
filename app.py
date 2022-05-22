# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(390, 640)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background: #F0F0F0")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 391, 441))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet("border:none;\n"
"outline:none;\n"
"display: flex;\n"
" justify-content: center;\n"
"background-color: #fff;")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.heart_widget = QtWidgets.QWidget(self.tab)
        self.heart_widget.setGeometry(QtCore.QRect(70, 70, 221, 181))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.heart_widget.setFont(font)
        self.heart_widget.setObjectName("heart_widget")
        self.label_4 = QtWidgets.QLabel(self.heart_widget)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(80, 10, 71, 71))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("icon/heart.png"))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.heart_rate_label = QtWidgets.QLabel(self.heart_widget)
        self.heart_rate_label.setGeometry(QtCore.QRect(60, 80, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.heart_rate_label.setFont(font)
        self.heart_rate_label.setAlignment(QtCore.Qt.AlignCenter)
        self.heart_rate_label.setObjectName("heart_rate_label")
        self.spo2_label = QtWidgets.QLabel(self.heart_widget)
        self.spo2_label.setGeometry(QtCore.QRect(60, 110, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.spo2_label.setFont(font)
        self.spo2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.spo2_label.setObjectName("spo2_label")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(140, 20, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("size: 16px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.alarm_time = QtWidgets.QDateTimeEdit(self.tab_2)
        self.alarm_time.setGeometry(QtCore.QRect(20, 90, 194, 22))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.alarm_time.setFont(font)
        self.alarm_time.setStyleSheet("background: #fff")
        self.alarm_time.setObjectName("alarm_time")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(20, 130, 47, 13))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.alarm_message = QtWidgets.QPlainTextEdit(self.tab_2)
        self.alarm_message.setGeometry(QtCore.QRect(20, 150, 321, 61))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.alarm_message.setFont(font)
        self.alarm_message.setStyleSheet("background: rgb(255, 255, 255)")
        self.alarm_message.setObjectName("alarm_message")
        self.btn_set_alarm = QtWidgets.QPushButton(self.tab_2)
        self.btn_set_alarm.setGeometry(QtCore.QRect(80, 240, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.btn_set_alarm.setFont(font)
        self.btn_set_alarm.setStyleSheet("background: white;\n"
"border: none;\n"
"border-radius: 10px")
        self.btn_set_alarm.setObjectName("btn_set_alarm")
        self.btn_cancel_set_alarm = QtWidgets.QPushButton(self.tab_2)
        self.btn_cancel_set_alarm.setGeometry(QtCore.QRect(190, 240, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Roboto")
        self.btn_cancel_set_alarm.setFont(font)
        self.btn_cancel_set_alarm.setStyleSheet("background: white;\n"
"border: none;\n"
"border-radius: 10px")
        self.btn_cancel_set_alarm.setObjectName("btn_cancel_set_alarm")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 391, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(-1)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("font-size: 16px;\n"
"text-decoration: underline;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setGeometry(QtCore.QRect(40, 70, 71, 16))
        self.label_6.setObjectName("label_6")
        self.lineEditPatientCode = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditPatientCode.setGeometry(QtCore.QRect(120, 70, 241, 20))
        self.lineEditPatientCode.setAutoFillBackground(False)
        self.lineEditPatientCode.setStyleSheet("border: 1px solid #888;")
        self.lineEditPatientCode.setText("")
        self.lineEditPatientCode.setFrame(True)
        self.lineEditPatientCode.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEditPatientCode.setDragEnabled(False)
        self.lineEditPatientCode.setReadOnly(True)
        self.lineEditPatientCode.setClearButtonEnabled(False)
        self.lineEditPatientCode.setObjectName("lineEditPatientCode")
        self.lineEditName = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditName.setGeometry(QtCore.QRect(120, 120, 241, 20))
        self.lineEditName.setAutoFillBackground(False)
        self.lineEditName.setStyleSheet("border: 1px solid black;")
        self.lineEditName.setObjectName("lineEditName")
        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setGeometry(QtCore.QRect(40, 120, 71, 16))
        self.label_7.setObjectName("label_7")
        self.lineEditPhone = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditPhone.setGeometry(QtCore.QRect(120, 170, 241, 20))
        self.lineEditPhone.setAutoFillBackground(False)
        self.lineEditPhone.setStyleSheet("border: 1px solid black;")
        self.lineEditPhone.setObjectName("lineEditPhone")
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(40, 170, 71, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(40, 260, 81, 16))
        self.label_9.setObjectName("label_9")
        self.textEditDisease = QtWidgets.QTextEdit(self.tab_3)
        self.textEditDisease.setGeometry(QtCore.QRect(120, 260, 241, 91))
        self.textEditDisease.setStyleSheet("border: 1px solid #888;")
        self.textEditDisease.setReadOnly(True)
        self.textEditDisease.setObjectName("textEditDisease")
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(40, 210, 71, 16))
        self.label_10.setObjectName("label_10")
        self.groupBox = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox.setGeometry(QtCore.QRect(110, 210, 241, 20))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radioButtonMale = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonMale.setGeometry(QtCore.QRect(10, 0, 82, 17))
        self.radioButtonMale.setChecked(True)
        self.radioButtonMale.setObjectName("radioButtonMale")
        self.radioButtonFemale = QtWidgets.QRadioButton(self.groupBox)
        self.radioButtonFemale.setGeometry(QtCore.QRect(140, 0, 82, 17))
        self.radioButtonFemale.setObjectName("radioButtonFemale")
        self.btnUpdate = QtWidgets.QPushButton(self.tab_3)
        self.btnUpdate.setGeometry(QtCore.QRect(270, 370, 91, 23))
        self.btnUpdate.setStyleSheet("border-radius: 4px;\n"
"border: 1px solid black;\n"
"color: white;\n"
"font-weight: bold;\n"
"background-color: #37455E;")
        self.btnUpdate.setObjectName("btnUpdate")
        self.tabWidget.addTab(self.tab_3, "")
        self.btn_speak = QtWidgets.QPushButton(self.centralwidget)
        self.btn_speak.setGeometry(QtCore.QRect(150, 450, 80, 80))
        self.btn_speak.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_speak.setAutoFillBackground(False)
        self.btn_speak.setStyleSheet("background: transparent;\n"
"")
        self.btn_speak.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/blue-mic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_speak.setIcon(icon1)
        self.btn_speak.setIconSize(QtCore.QSize(64, 64))
        self.btn_speak.setObjectName("btn_speak")
        self.btn_send_4 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send_4.setGeometry(QtCore.QRect(340, 570, 41, 41))
        self.btn_send_4.setAutoFillBackground(False)
        self.btn_send_4.setStyleSheet("background: transparent;\n"
"")
        self.btn_send_4.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(".icon/send.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_send_4.setIcon(icon2)
        self.btn_send_4.setIconSize(QtCore.QSize(32, 32))
        self.btn_send_4.setObjectName("btn_send_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 570, 321, 41))
        self.lineEdit_4.setStyleSheet("background: transparent;\n"
"border: 1px solid black;\n"
"border-raidus: 10px;")
        self.lineEdit_4.setDragEnabled(False)
        self.lineEdit_4.setObjectName("lineEdit_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Healthcare Virtual Assistant"))
        self.heart_rate_label.setText(_translate("MainWindow", "Your heart rate is "))
        self.spo2_label.setText(_translate("MainWindow", "Your spo2 is"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Chat"))
        self.label.setText(_translate("MainWindow", "Alarm"))
        self.label_2.setText(_translate("MainWindow", "Time"))
        self.label_3.setText(_translate("MainWindow", "Message"))
        self.btn_set_alarm.setText(_translate("MainWindow", "OK"))
        self.btn_cancel_set_alarm.setText(_translate("MainWindow", "Cancel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Alarm"))
        self.label_5.setText(_translate("MainWindow", "Patient Information"))
        self.label_6.setText(_translate("MainWindow", "Patient Code:"))
        self.lineEditPatientCode.setPlaceholderText(_translate("MainWindow", "Patient code..."))
        self.lineEditName.setPlaceholderText(_translate("MainWindow", "..."))
        self.label_7.setText(_translate("MainWindow", "Name:"))
        self.lineEditPhone.setPlaceholderText(_translate("MainWindow", "..."))
        self.label_8.setText(_translate("MainWindow", "Phone:"))
        self.label_9.setText(_translate("MainWindow", "Disease Infor:"))
        self.textEditDisease.setPlaceholderText(_translate("MainWindow", "..."))
        self.label_10.setText(_translate("MainWindow", "Sex:"))
        self.radioButtonMale.setText(_translate("MainWindow", "Male"))
        self.radioButtonFemale.setText(_translate("MainWindow", "Female"))
        self.btnUpdate.setText(_translate("MainWindow", "Update"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Information"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "Ask me"))





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

