import serial
import time
import virtual_assistant
import asyncio


# Parameters:
# port: tên cổng nối với arduino
# baudrate: tốc độ baud ví dụ như 9600 hoạch 11520


def init_sensor():
    arduino_data = None
    try:
        arduino_data = serial.Serial('COM3', 115200)
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
    print(string_data)
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


def measure(arduino_data):
    raw_data = []
    flag = True
    timeout = time.time() + 10

    while flag:
        data_from_sensor = read_sensor(arduino_data)
        print(data_from_sensor)
        # if 'No finger' in data_from_sensor:
        #     raw_data.clear()
        #     timeout = None
        #     # print('Please put your finger on the sensor')
        #
        # elif data_from_sensor.__len__() == 0:
        #     continue
        # else:
        #     if timeout is None:
        #         timeout = time.time() + 15
        #
        if time.time() > timeout:
            flag = False
        # else:
        # if count > 10 * 10000000000000000:
        #     flag = False
        else:
            # count += 1
            raw_data.append(data_from_sensor)

        time.sleep(1)

    data = raw_data[raw_data.__len__() - 1]
    array = data.split(",")
    virtual_assistant.speak("Your heart rate is " + array[0] + " bpm")
    virtual_assistant.speak("and the spo2 is " + array[array.__len__() - 1] + " percent")


if __name__ == "__main__":  # chỉ chạy các chức năng có trong file sensor và không chạy trong các file khác
    arduino = init_sensor()
    # while True:
    #     read_sensor(arduino)
    measure(arduino)
