import datetime
import sys
import time
import uuid
from datetime import *

import pyttsx3 as pyttsx3
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import ReadWrite
import account
import firebase_database
import prompt_dialog
import signin_form
import signup_form
from ReadWrite import Alarm
from SensorData import SensorData
from account import Login
# from virtual_assistant import introduce
from sensor import read_sensor
from virtual_assistant import speak
from virtual_assistant_2 import *
from alarm_dialog import Ui_Dialog
import speech_recognition as sr
import playsound
from PyQt5 import QtCore, QtGui, QtWidgets
from firebase_database import *
from app import Ui_MainWindow
import pyrebase

global command
command = ""

from sendmail import sendemail

# from account import Login
# from account import CreateAcc

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "n18dccn237java@gmail.com"  # Enter your address nqubjcnsenjyrppp
receiver_email = "luutienphat@gmail.com"  # Enter receiver addresspassword
password = "dqocoxgxjylgooqg"
# password = input("Type your password and press enter: ")
message = """\
Subject: Hi doctor

Patient is showing signs of poor health. """

from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
account_sid = 'AC98b3f8f8743972146b1f706fcdd4cf63'
auth_token = '14f22c92a29e83fe060322687cb98d4f'


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

        # save data to firebase database
        data = {"user": "temp", "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "hr": avg_heart_rate, "spo2": raw_data[raw_data.__len__() - 1].spo2}
        db.child("MeasurementHistory").push(data)
        if int(avg_heart_rate) > 100 or int(raw_data[raw_data.__len__() - 1].spo2) <= 90:
            try:
                sendemail(port, sender_email, receiver_email, password, message + data)
                client = Client(account_sid, auth_token)
                message1 = client.messages.create(
                    body=message + data,
                    from_='+18507905695',
                    to='+84386201456'
                )
                print(message1.body)
            except Exception:
                print("Sorry ! You are dividing by zero ")

    def stop(self):
        print('Stopping thread', self.index)
        self.arduino_data.close()
        self.terminate()


class AlarmItem(QWidget):
    def __init__(self, parent=None, alarm=None):
        super(AlarmItem, self).__init__()
        self.parent = parent
        self.alarm = alarm
        self.row = QHBoxLayout()

        self.column2 = QVBoxLayout()
        self.column2.setAlignment(Qt.AlignHCenter)
        clock = QLabel("clock")
        # clock.setGeometry(QtCore.QRect(10, 9, 31, 31))
        clock.setText("")
        clock.setPixmap(QtGui.QPixmap("icon/clock.png"))
        clock.setAlignment(QtCore.Qt.AlignCenter)
        self.column2.addWidget(clock)

        if alarm.is_once:
            self.column2.addWidget(QLabel("Once"))
        else:
            self.column2.addWidget(QLabel("Everyday"))

        pushButton = QtWidgets.QPushButton()
        # pushButton.setGeometry(QtCore.QRect(240, 12, 31, 23))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        pushButton.setIcon(icon2)
        pushButton.clicked.connect(self.onClick)
        self.row.addItem(self.column2)

        self.column = QVBoxLayout()
        self.column.addWidget(QLabel(self.alarm.__get_time__()))
        self.column.addWidget(QLabel(self.alarm.message))
        self.row.addItem(self.column)
        self.row.addWidget(pushButton)
        self.setLayout(self.row)
        # self.setStyleSheet("margin-bottom: 1px;\nborder:none;\npadding:0")
        self.setStyleSheet(
            "background: transparent;\nborder-radius: 10px;\nmargin-bottom: 1px;\nborder:none;\npadding:0")

    def onClick(self):
        print("clicked")
        alarm_list = ReadWrite.readFile()
        al = None
        for a in alarm_list:
            if a.uuid == self.alarm.uuid:
                al = a
                break
        alarm_list.remove(al)
        ReadWrite.writeFile(alarm_list)
        self.parent.fill_alarm_list()


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


# speak
class ThreadClass4(QThread):
    # voice_data_signal = pyqtSignal(str)
    # error_signal = pyqtSignal(str)

    def __init__(self, index=0, text=""):
        super().__init__()
        self.text = text
        self.index = index
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # voices[0]: male voice, voices[1]: female voice

    def run(self):
        try:
            if self.engine._inLoop:
                self.engine.endLoop()

            if self.text.strip().__len__() != 0:
                self.engine.say(self.text)
                self.engine.runAndWait()

        except Exception as e:
            print("speak error ")

    def stop(self):
        print('Stopping thread', self.index)
        try:
            self.engine.endLoop()
            self.engine.stop()
        except Exception as e:
            print("stop speak error ")
        self.terminate()


class ThreadClass5(QThread):
    open_prompt_signal = pyqtSignal(object)
    delete_alarm_signal = pyqtSignal(object)

    def __init__(self, index=0, alarm=None):
        super().__init__()
        self.index = index
        self.alarm = alarm

    def run(self):
        while True:
            time.sleep(1)
            current_time = datetime.now()
            now = current_time.strftime("%H:%M")
            date = current_time.strftime("%d/%m/%Y")
            # print("index: ", self.index)
            # print("The Set Date is:", date)
            # print("Thời gian hiện tại", now)
            alarm_time = datetime.strptime(self.alarm.__get_time__(), '%H:%M')
            alarm_time_str = alarm_time.strftime("%H:%M")
            # print("Thời gian báo thưc", alarm_time_str)
            if now == alarm_time_str:
                # print("Tin nhắn", self.alarm.message)
                self.open_prompt_signal.emit(self.alarm)
                # playsound.playsound("sound")
                if self.alarm.is_once:
                    self.delete_alarm_signal.emit(self.alarm)
                    break

    def stop(self):
        print('Stopping thread', self.index)
        self.terminate()


class AlarmDialog(QDialog):
    def __init__(self, parent=None):
        super(AlarmDialog, self).__init__(parent)
        self.main_win = QDialog()
        self.parent = parent
        self.uic = Ui_Dialog()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.uic.setupUi(self)
        self.uic.btn_cancel_set_alarm.clicked.connect(self.on_click_btn_cancel_set_alarm)
        self.uic.btn_set_alarm.clicked.connect(self.on_click_btn_set_alarm)

    def on_click_btn_set_alarm(self):
        hour = self.uic.alarm_time.time().hour()
        minute = self.uic.alarm_time.time().minute()
        is_once = self.uic.isOnce.isChecked()
        message = self.uic.alarm_message.toPlainText()

        alarm = Alarm(uuid=uuid.uuid4(), hour=hour, minute=minute, message=message, is_once=is_once)
        alarm_list = ReadWrite.readFile()
        alarm_list.append(alarm)
        ReadWrite.writeFile(alarm_list)
        print(len(alarm_list))
        self.parent.fill_alarm_list()
        self.close()

    def on_click_btn_cancel_set_alarm(self):
        self.close()
        print()


class PromptDialog(QDialog):
    def __init__(self, parent=None, alarm=None):
        super(PromptDialog, self).__init__(parent)
        self.main_win = QDialog()
        self.parent = parent
        self.alarm = alarm
        self.uic = prompt_dialog.Ui_Dialog()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.uic.setupUi(self)
        self.uic.btn_ok.clicked.connect(self.on_click_btn_ok)
        self.uic.time_label.setText(self.alarm.__get_time__())
        self.uic.message_label.setText(self.alarm.message)
        playsound.playsound(sound='sound/good-morning.mp3', block=False)

    def on_click_btn_ok(self):
        self.main_win.close()


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
        self.uic.btn_speak.clicked.connect(self.on_click_speak_button)
        self.uic.btnUpdate.clicked.connect(self.updatePatient)
        self.uic.btnSignout.clicked.connect(self.goto_signin)
        self.uic.tabWidget.tabBarClicked.connect(self.get_measurement_history_data)

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

        # item1 = AlarmItem(self.uic.alarm_list)
        # self.uic.alarm_list.addItem(item1)
        # self.uic.alarm_list.addItem(item1)

        self.fill_alarm_list()

        self.uic.btn_active.clicked.connect(
            lambda: self.speak("Hi, I'm your healthcare virtual assistant. \nWhat can I do for you?"))
        self.uic.btn_new_alarm.clicked.connect(self.on_click_btn_new_alarm)
        self.alarm_dialog = None
        threading.Thread(target=self.introduce2, daemon=True).start()
        self.uic.alarm_list.setStyleSheet("QListWidget::item {"
                                          "border:none;"
                                          "background-color: white;"
                                          "border-radius: 10px;"
                                          "margin-bottom: 5px"
                                          "}"
                                          "QListWidget::item:selected {"
                                          "background-color: #DDD;"
                                          "}")
        self.uic.stop_all.clicked.connect(self.cancel_all_alarm)
        self.uic.stop_all.hide()

        self.uic.btn_submit.clicked.connect(self.on_btn_summit_click)

    def cancel_all_alarm(self):
        for i in self.alarm_thread:
            self.alarm_thread[i].stop()
        self.alarm_thread.clear()

    def fill_alarm_list(self):
        self.cancel_all_alarm()
        self.uic.alarm_list.clear()
        alarm_list = ReadWrite.readFile()
        i = 0
        for alarm in alarm_list:
            item = QListWidgetItem(self.uic.alarm_list)
            self.uic.alarm_list.addItem(item)
            row = AlarmItem(parent=self, alarm=alarm)
            item.setSizeHint(row.minimumSizeHint())
            self.uic.alarm_list.setItemWidget(item, row)
            self.alarm_thread[i] = ThreadClass5(index=i, alarm=alarm)
            self.alarm_thread[i].start()
            self.alarm_thread[i].open_prompt_signal.connect(self.open_prompt)
            self.alarm_thread[i].delete_alarm_signal.connect(self.delete_alarm)
            i += 1

    def open_prompt(self, open_prompt_signal):
        promptDialog = PromptDialog(alarm=open_prompt_signal)
        promptDialog.exec_()

    def delete_alarm(self, delete_alarm_signal):
        alarm_list = ReadWrite.readFile()
        al = None
        for a in alarm_list:
            if a.uuid == delete_alarm_signal.uuid:
                al = a
                break
        alarm_list.remove(al)
        ReadWrite.writeFile(alarm_list)
        self.fill_alarm_list()

    def goto_signin(self):
        # signInForm = SignInForm()
        # signInForm.show()
        # self.main_win.close()
        self.showSignInForm()

    def speak(self, text):
        if self.is_speaking:
            self.is_speaking = not self.is_speaking
            self.thread[4].stop()
            return

        self.is_speaking = not self.is_speaking
        self.thread[4] = ThreadClass4(index=1, text=text)
        self.thread[4].start()

    def on_btn_summit_click(self):
        height = int(self.uic.edit_height.text())
        weight = int(self.uic.edit_height.text())
        self.bmi2(height=height, weight=weight)

    def bmi2(self, height, weight):
        result = weight / (height * height)
        status = ""
        if result < 16:
            status = 'Severe thinness'
        elif result >= 16 & result < 17:
            status = 'moderate thinness '
        elif result >= 17 & result < 18.5:
            status = 'thin'
        elif result >= 18.5 & result < 25:
            status = 'normal'
        elif result >= 25 & result < 30:
            status = 'overweight'
        elif result >= 30 & result < 35:
            status = 'Obese type 1'
        elif result >= 35 & result < 40:
            status = 'Obese type 2'
        else:
            status = 'Obese type 3'

        self.uic.label_status.setText("You are: " + status)
        self.uic.label_bmi_index.setText("Your BMI Index: " + str(result))
        self.speak("You are in " + status + " status")

    def measureHeartRate(self):
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

        firebase = pyrebase.initialize_app(firebase_database.firebaseConfig)
        database = firebase.database()

        data = {"patientCode": code, "patientName": name, "patientSex": sex, "patientPhone": phone,
                "patientDisease": disease}

        patient = database.child("PatientInformation").child(code).get()
        print(patient)

        if patient.val() != "" or patient.val() != None:
            print("exist")
            database.child("PatientInformation").child(code).update(data)
        else:
            print("notexist")
            database.child("PatientInformation").child(code).set(data)

    def changBtnSpeakIcon(self, icon_type=True):
        if icon_type:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("icon/blue-mic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.uic.btn_speak.setIcon(icon1)
            self.uic.btn_speak.setIconSize(QtCore.QSize(48, 48))
        else:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("icon/voice-wave.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.uic.btn_speak.setIcon(icon1)
            self.uic.btn_speak.setIconSize(QtCore.QSize(48, 48))

    def on_click_speak_button(self):
        if self.is_btn_speak_clicked:
            self.is_btn_speak_clicked = not self.is_btn_speak_clicked
            self.thread[3].stop()
            self.changBtnSpeakIcon(icon_type=True)
            return

        self.is_btn_speak_clicked = not self.is_btn_speak_clicked

        playsound.playsound('sound/data_2.wav')
        self.changBtnSpeakIcon(icon_type=False)
        self.thread[3] = ThreadClass3(index=1)
        self.thread[3].start()
        self.thread[3].voice_data_signal.connect(self.finishHearing)
        self.thread[3].error_signal.connect(self.errorWhileHearing)
        # threading.Thread(target=listen2(self)).start()

    def get_measurement_history_data(self, index):
        # index == 3: tab_history
        if index == 3:
            self.uic.listWidget_history.clear()
            temp = db.child("MeasurementHistory").get().val()
            for x in temp:
                date = temp[x]['date']
                hr = temp[x]['hr']
                spo2 = temp[x]['spo2']
                item = QListWidgetItem()
                self.uic.listWidget_history.addItem(item)
                item.setText("HR: {} bpm, spo2: {}% | {}".format(hr, spo2, date))

    def finishHearing(self, voice_data_signal):
        self.uic.chat_user.setText(voice_data_signal)
        self.speechRunnable = SpeechRunnable()
        respond2(self, voice_data_signal)
        self.changBtnSpeakIcon(icon_type=True)
        # speak(voice_data_signal)

    def errorWhileHearing(self, error_signal):
        self.uic.chat_user.setText("...")
        self.uic.chat_bot.setText(error_signal)
        self.changBtnSpeakIcon(icon_type=True)

    def on_click_send(self):
        self.uic.tabWidget.setCurrentWidget(self.uic.tab)
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

    def on_click_btn_new_alarm(self):
        dialog = AlarmDialog(parent=self)
        dialog.exec_()

    def introduce2(self):
        self.uic.chat_bot.setText("Hi, I'm your healthcare virtual assistant. \nWhat can I do for you?")
        playsound.playsound('sound/cortana_sound_effect.mp3')
        self.speechRunnable = SpeechRunnable()
        self.speechRunnable.speak("Hi, I'm your healthcare virtual assistant. What can I do for you?")


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
        email = self.uic.email.text()
        user_password = self.uic.password.text()
        try:
            ref = account.auth.sign_in_with_email_and_password(email, user_password)
            print(ref['localId'])
            mainWindow = MainWindow()
            mainWindow.show()
            self.main_win.close()

        except Exception as e:
            self.uic.invalid.setVisible(True)

    def goto_create(self):
        self.showSignUpForm()

    def showSignUpForm(self):
        self.main_win.close()
        self.sub_win = QMainWindow()
        self.uic1 = signup_form.Ui_MainWindow()
        self.uic1.setupUi(self.sub_win)
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
        # signInForm = SignInForm()
        # signInForm.show()
        # self.main_win.close()
        self.showSignInForm()

    def create_acc_function(self):
        email = self.uic.email.text()
        if self.uic.password.text() == self.uic.confirmpass.text():
            user_password = self.uic.password.text()
            try:
                account.auth.create_user_with_email_and_password(email, user_password)
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


def main():
    app = QApplication(sys.argv)
    # main_win = MainWindow()
    # main_win.show()
    signInForm = SignInForm()
    signInForm.show()
    # main_win = MainWindow()
    # main_win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# if __name__ == "__main__":
#     window.after(500, introduce)  # after mainloop() 500ms, call introduce()
#     window.mainloop()
