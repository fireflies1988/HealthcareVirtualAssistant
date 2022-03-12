import threading
from tkinter import *

import serial
import time

import ui
import virtual_assistant
import threading
import asyncio

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
        # print(data_from_sensor)
        data = data_from_sensor.split(",")
        if data.__len__() > 1:
            if data_from_sensor.__contains__("0,0"):
                timeout = None
                raw_data.clear()
                count += 1

                if count > 5:
                    ui.measure_label.place(relx=-0.5, rely=-1.0, anchor=N, y=120)
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
            else:
                # if data[1] == 0 or data[1] == 0:
                #     continue
                # else:
                sensor_data = SensorData(heart_rate=data[0], spo2=data[1])
                raw_data.append(sensor_data)

                # ui control
                ui.heart_button.place(relx=0.5, rely=0.0, y=50, anchor=N)
                ui.warning_label.place(relx=-0.5, rely=-1.0, anchor=N, y=120)  # destroy warning label
                ui.measure_label.place(relx=0.5, rely=0.0, anchor=N, y=120)  # init measuring label

        time.sleep(1)

    sum_heart_rate = 0
    for d in raw_data:
        sum_heart_rate += int(d.heart_rate)

    avg_heart_rate = int(sum_heart_rate / raw_data.__len__())

    # ui control
    ui.heart_rate_label = Label(ui.window, text=f"Your average heart rate is {avg_heart_rate}bpm",
                                font=("Roboto", 14), padx=10)
    ui.heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
    ui.spo2_label = Label(ui.window, text=f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2}%", font=("Roboto", 14), padx=10)
    ui.spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=160)

    virtual_assistant.speak(f"Your average heart rate is {avg_heart_rate} bpm")
    virtual_assistant.speak(f"Your spo2 is {raw_data[raw_data.__len__() - 1].spo2} percent")


def measure_max30102(arduino_data):
    raw_data = []
    flag = True
    timeout = None

    while flag:
        data_from_sensor = read_sensor(arduino_data)
        print(data_from_sensor)
        if 'No finger' in data_from_sensor:
            raw_data.clear()
            timeout = None
            # print('Please put your finger on the sensor')

        elif data_from_sensor.__len__() == 0:
            continue
        else:
            if timeout is None:
                timeout = time.time() + 15

        if time.time() > timeout:
            flag = False
        else:
            raw_data.append(data_from_sensor)

    data = raw_data[raw_data.__len__() - 1]
    array = data.split(",")
    virtual_assistant.speak("Your heart rate is " + array[0] + " bpm")


if __name__ == "__main__":  # chỉ chạy các chức năng có trong file sensor và không chạy trong các file khác
    arduino = init_sensor()
    # while True:
    #     read_sensor(arduino)
    measure_max30100(arduino)
