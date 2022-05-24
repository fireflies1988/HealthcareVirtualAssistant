import threading
from datetime import date
from tkinter import *

import serial
import time

import ui
import threading
import asyncio

import virtual_assistant
from SensorData import SensorData



def init_sensor():
    arduino_data = None
    try:
        arduino_data = serial.Serial('COM3', 115200)
        # Parameters:
        # port: tên cổng nối với arduino
        # baudrate: tốc độ baud ví dụ như 9600 hoạch 11520
    except serial.SerialException:
        arduino_data = None
        pass
    except():
        arduino_data = None
        pass
    return arduino_data


def read_sensor(arduino_data):  # đọc dữ liệu từ cổng serial
    string_data = ""
    if arduino_data.inWaiting() > 0:
        data_packet = arduino_data.readline()
        # print(data_packet)
        try:
            string_data = data_packet.decode()  # convert from binary string  to string
        except UnicodeEncodeError:
            pass
        except:
            pass
        string_data = string_data.strip('\r\n')  # remove '\r\n' characters

    elif arduino_data.inWaiting() == 0:  # gonna check if arduino has data yet (0: no data, > 0: has data)
        return ""
    # print(string_data)
    return string_data


def switch_sensor(order, arduino_data):  # switch on/off sensor (still in development)
    if arduino_data.inWaiting() > 0:
        if order == 'ON':
            arduino_data.write('On sensor')
        else:
            arduino_data.write('Off sensor')


def switch_arduino(order, arduino_data):  # bật tắt arduino, input vào là 'ON' hoặc 'OFF'
    if order == 'ON':
        arduino_data.write('On sensor')
        arduino_data.open()
    else:
        arduino_data.write('Off sensor')
        arduino_data.close()


def read_temperature(arduino_data):
    flag = True
    while flag:
        data_from_sensor = read_sensor(arduino_data)
        sensor_data = data_from_sensor.split(",")

        if sensor_data[4] is not None or sensor_data[4] != "0":
            flag = False
            virtual_assistant.speak(f"The temperature is ${sensor_data[4]}")


# def read_heart_rate():
#     if arduino_data.inWaiting() > 0:
#         read_sensor()
#
#
# def read_spo2_rate():
#     if arduino_data.inWaiting() > 0:
#         my_data = arduino_data.readline()
#         string_data = my_data.decode('ascii')
#         print(string_data)

def measure_max30100(arduino_data):
    raw_data = []
    flag = True
    timeout = None
    count = 0

    while flag:
        data_from_sensor = read_sensor(arduino_data)
        print(data_from_sensor)
        data = data_from_sensor.split(",")
        if data.__len__() > 1:  # chỉ lấy dữ liệu có đầy đủ cả hai phần tử
            if data[0] == "0" or data[1] == "0":
                timeout = None
                raw_data.clear()
                count += 1

                if count > 5:
                    ui.measure_label.place_forget()
                    ui.warning_label.place_forget()
                    ui.heart_rate_label.place_forget()
                    ui.spo2_label.place_forget()

                    # ui.measure_label.place(relx=-0.5, rely=-1.0, anchor=N, y=120)
                    ui.warning_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
                    virtual_assistant.speak("Place your index finger on the sensor")
                    # thread = threading.Thread(
                    #     target=virtual_assistant.speak("Place your index finger on sensor")).start()
                    count = 0
                continue

            if timeout is None:
                timeout = time.time() + 20

            if time.time() > timeout:
                flag = False

            else:  # khi mọi thứ đã hoàn hảo
                sensor_data = SensorData(heart_rate=data[0], spo2=data[1])
                raw_data.append(sensor_data)

                # ui control
                ui.heart_button.place(relx=0.5, rely=0.0, y=50, anchor=N)
                # ui.warning_label.place(relx=-0.5, rely=-1.0, anchor=N, y=120)  # destroy warning label

                ui.measure_label.place_forget()
                ui.warning_label.place_forget()
                ui.heart_rate_label.place_forget()
                ui.spo2_label.place_forget()

                ui.measure_label.place(relx=0.5, rely=0.0, anchor=N, y=120)  # init measuring label

                # ui.heart_rate_label = Label(ui.window, text=f"Your heart rate is {sensor_data.heart_rate}bpm",
                #                             font=("Roboto", 14), padx=10)
                # ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
                # ui.spo2_label = Label(ui.window, text=f"Your spo2 is {sensor_data.spo2}%",
                #                       font=("Roboto", 14),
                #                       padx=10)
                # ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

        time.sleep(1)

    # tính toán nhịp tim trung bình
    sum_heart_rate = 0
    for d in raw_data:
        sum_heart_rate += int(d.heart_rate)

    avg_heart_rate = int(sum_heart_rate / raw_data.__len__())

    # ui control
    ui.measure_label.place_forget()
    ui.warning_label.place_forget()
    ui.heart_rate_label.place_forget()
    ui.spo2_label.place_forget()

    ui.heart_rate_label.place(relx=-1.0, rely=-1.0, anchor=N)
    ui.heart_rate_label = Label(ui.window, text=f"Your average heart rate is {avg_heart_rate}bpm",
                                font=("Roboto", 14), padx=10)
    ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
    ui.spo2_label = Label(ui.window, text=f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2}%", font=("Roboto", 14),
                          padx=10)
    ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

    virtual_assistant.speak(f"Your average heart rate is {avg_heart_rate} bpm")
    virtual_assistant.speak(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")


def measure_max30100_2(arduino_data, self):
    raw_data = []
    flag = True
    timeout = None
    count = 0

    while flag:
        data_from_sensor = read_sensor(arduino_data)
        print(data_from_sensor)
        data = data_from_sensor.split(",")
        if data.__len__() > 1:  # chỉ lấy dữ liệu có đầy đủ cả hai phần tử
            if data[0] == "0" or data[1] == "0":
                timeout = None
                raw_data.clear()
                count += 1

                if count > 10:
                    # ui.measure_label.place_forget()
                    # ui.warning_label.place_forget()
                    # ui.heart_rate_label.place_forget()
                    # ui.spo2_label.place_forget()
                    #
                    # # ui.measure_label.place(relx=-0.5, rely=-1.0, anchor=N, y=120)
                    # ui.warning_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
                    self.uic.heart_widget.setEnabled(False)
                    self.uic.heart_rate_label.show()
                    self.uic.heart_rate_label.setText("Place your index finger on the sensor")
                    # self.speechRunnable.speak("Place your index finger on the sensor")
                    # thread = threading.Thread(
                    #     target=virtual_assistant.speak("Place your index finger on sensor")).start()
                    count = 0
                continue

            if timeout is None:
                timeout = time.time() + 20

            if time.time() > timeout:
                flag = False

            else:  # khi mọi thứ đã hoàn hảo
                sensor_data = SensorData(heart_rate=data[0], spo2=data[1])
                raw_data.append(sensor_data)

                # ui control
                # ui.heart_button.place(relx=0.5, rely=0.0, y=50, anchor=N)
                # ui.warning_label.place(relx=-0.5, rely=-1.0, anchor=N, y=120)  # destroy warning label

                # ui.measure_label.place_forget()
                # ui.warning_label.place_forget()
                # ui.heart_rate_label.place_forget()
                # ui.spo2_label.place_forget()

                # ui.measure_label.place(relx=0.5, rely=0.0, anchor=N, y=120)  # init measuring label

                self.uic.heart_widget.setEnabled(True)
                self.uic.heart_rate_label.show()
                self.uic.heart_rate_label.setText("Measuring")

                # ui.heart_rate_label = Label(ui.window, text=f"Your heart rate is {sensor_data.heart_rate}bpm",
                #                             font=("Roboto", 14), padx=10)
                # ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
                # ui.spo2_label = Label(ui.window, text=f"Your spo2 is {sensor_data.spo2}%",
                #                       font=("Roboto", 14),
                #                       padx=10)
                # ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

        time.sleep(1)

    # tính toán nhịp tim trung bình
    sum_heart_rate = 0
    for d in raw_data:
        sum_heart_rate += int(d.heart_rate)

    avg_heart_rate = int(sum_heart_rate / raw_data.__len__())

    # ui control
    # ui.measure_label.place_forget()
    # ui.warning_label.place_forget()
    # ui.heart_rate_label.place_forget()
    # ui.spo2_label.place_forget()
    #
    # ui.heart_rate_label.place(relx=-1.0, rely=-1.0, anchor=N)
    # ui.heart_rate_label = Label(ui.window, text=f"Your average heart rate is {avg_heart_rate}bpm",
    #                             font=("Roboto", 14), padx=10)
    # ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
    # ui.spo2_label = Label(ui.window, text=f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2}%", font=("Roboto", 14),
    #                       padx=10)
    # ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

    self.uic.heart_widget.setEnabled(True)
    self.uic.heart_rate_label.show()
    self.uic.spo2_label.show()
    self.uic.heart_rate_label.setText(f"Your average heart rate is {avg_heart_rate} bpm")
    self.uic.spo2_label.setText(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")

    # self.speechRunnable.speak(f"Your average heart rate is {avg_heart_rate} bpm")
    # self.speechRunnable.speak(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")


def     measure_max30102(arduino_data):
    raw_data = []
    flag = True
    timeout = None
    count = 0

    while flag:
        data_from_sensor = read_sensor(arduino_data)
        print(data_from_sensor)
        if 'No finger' in data_from_sensor:
            count += 1

            if count > (5 * 1000):
                count = 0
                raw_data.clear()

                ui.measure_label.place_forget()
                ui.warning_label.place_forget()
                ui.heart_rate_label.place_forget()
                ui.spo2_label.place_forget()

                ui.warning_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
                virtual_assistant.speak("Place your index finger on the sensor")

        elif data_from_sensor.__len__() == 0:
            continue
        else:
            if timeout is None:
                timeout = time.time() + 15

        if time.time() > timeout:
            flag = False
        else:
            data_split = data_from_sensor.split(",")
            sensor_data = SensorData(heart_rate=data_split[0], average_heart_rate=data_split[1], spo2=data_split[2])
            raw_data.append(sensor_data)

            ui.heart_button.place(relx=0.5, rely=0.0, y=50, anchor=N)

            ui.measure_label.place_forget()
            ui.warning_label.place_forget()
            ui.heart_rate_label.place_forget()
            ui.spo2_label.place_forget()

            ui.measure_label.place(relx=0.5, rely=0.0, anchor=N, y=120)  # init measuring label

    data = raw_data[raw_data.__len__() - 1]
    array = data.split(",")
    virtual_assistant.speak("Your heart rate is " + array[0] + " bpm")

    # ui control
    ui.measure_label.place_forget()
    ui.warning_label.place_forget()
    ui.heart_rate_label.place_forget()
    ui.spo2_label.place_forget()

    ui.heart_rate_label.place_forget()
    ui.heart_rate_label = Label(ui.window,
                                text=f"Your average heart rate is {raw_data[raw_data.__len__() - 1].average_heart_rate}bpm",
                                font=("Roboto", 14), padx=10)
    ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)

    ui.spo2_label = Label(ui.window, text=f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2}%", font=("Roboto", 14),
                          padx=10)
    ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

    virtual_assistant.speak(f"Your average heart rate is {raw_data[raw_data.__len__() - 1]} bpm")
    virtual_assistant.speak(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")



def measure_max30102_df_robot(arduino_data):
    raw_data = []
    flag = True
    timeout = None
    count = 0

    while flag:
        data_from_sensor = read_sensor(arduino_data)
        print(data_from_sensor)
        if 'No finger' in data_from_sensor:
            count += 1

            if count > (5 * 1000):
                count = 0
                raw_data.clear()

                ui.measure_label.place_forget()
                ui.warning_label.place_forget()
                ui.heart_rate_label.place_forget()
                ui.spo2_label.place_forget()

                ui.warning_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
                virtual_assistant.speak("Place your index finger on the sensor")

        elif data_from_sensor.__len__() == 0:
            continue
        else:
            if timeout is None:
                timeout = time.time() + 15

        if time.time() > timeout:
            flag = False
        else:
            data_split = data_from_sensor.split(",")
            sensor_data = SensorData(heart_rate=data_split[0], average_heart_rate=data_split[1], spo2=data_split[2])
            raw_data.append(sensor_data)

            ui.heart_button.place(relx=0.5, rely=0.0, y=50, anchor=N)

            ui.measure_label.place_forget()
            ui.warning_label.place_forget()
            ui.heart_rate_label.place_forget()
            ui.spo2_label.place_forget()

            ui.measure_label.place(relx=0.5, rely=0.0, anchor=N, y=120)  # init measuring label

    data = raw_data[raw_data.__len__() - 1]
    array = data.split(",")
    virtual_assistant.speak("Your heart rate is " + array[0] + " bpm")

    # ui control
    ui.measure_label.place_forget()
    ui.warning_label.place_forget()
    ui.heart_rate_label.place_forget()
    ui.spo2_label.place_forget()

    ui.heart_rate_label.place_forget()
    ui.heart_rate_label = Label(ui.window,
                                text=f"Your average heart rate is {raw_data[raw_data.__len__() - 1].average_heart_rate}bpm",
                                font=("Roboto", 14), padx=10)
    ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)

    ui.spo2_label = Label(ui.window, text=f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2}%", font=("Roboto", 14),
                          padx=10)
    ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

    virtual_assistant.speak(f"Your average heart rate is {raw_data[raw_data.__len__() - 1]} bpm")
    virtual_assistant.speak(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")


if __name__ == "__main__":  # chỉ chạy các chức năng có trong file sensor và không chạy trong các file khác
    arduino = init_sensor()
    # measure_max30100(arduino)
    measure_max30102(arduino)
