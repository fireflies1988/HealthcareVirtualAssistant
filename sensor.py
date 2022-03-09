import time
import speech_recognition as sr
import serial
import pyttsx3
import asyncio

# Khởi tạo phần giọng nói cho ứng dụng
ann = pyttsx3.init()  # Khởi tạo dịch vụ pyttsx3
voices = ann.getProperty('voices')  # Sử dụng gói giọng nói trong pyttsx3
ann.setProperty('voice', voices[1].id)  # Sử dụng giọng nữ cho gói giọng nói này

# Parameters:
# port: tên cổng nối với arduino
# baudrate: tốc độ baud ví dụ như 9600 hoạch 11520

arduino_data = serial.Serial('COM3', 115200)  # Khởi tạo cổng mà kết nối tới Adruino


def read_sensor():  # đọc dữ liệu từ cảm biến
    string_data = ""
    if arduino_data.inWaiting() > 0:
        data_packet = arduino_data.readline()
        try:
            string_data = data_packet.decode()  # convert from binary string  to string
            string_data = string_data.strip('\r\n')  # remove '\r\n' characters
        except UnicodeEncodeError:
            pass

    elif arduino_data.inWaiting() == 0:  # gonna check if arduino has data yet (0: no data, > 0: has data)
        return ""
    return string_data


def switch_sensor(order):  # switch on/off sensor (still in development)
    if arduino_data.inWaiting() > 0:
        if order == 'ON':
            arduino_data.write('On sensor')
        else:
            arduino_data.write('Off sensor')


def switch_arduino(order):  # bật tắt arduino, input vào là 'ON' hoặc 'OFF'
    if order == 'ON':
        arduino_data.write('On sensor')
        arduino_data.open()
    else:
        arduino_data.write('Off sensor')
        arduino_data.close()


def read_heart_rate():
    if arduino_data.inWaiting() > 0:
        read_sensor()


def read_spo2_rate():
    if arduino_data.inWaiting() > 0:
        my_data = arduino_data.readline()
        string_data = my_data.decode('ascii')
        print(string_data)


def command():
    c = sr.Recognizer()  # Khởi tạo nhận diện giọng nói
    with sr.Microphone() as source:  # Nguồn giọng nói đầu vào lấy từ Microphone
        # c.pause_threshold = 1  # thời gian chờ là 1s
        c.adjust_for_ambient_noise(source, duration=1)  # giảm tiếng ồn từ môi trường
        c.energy_threshold = 1000

        print('Listening...')
        speak('Listening...')

        audio = c.listen(source, timeout=10)  # the program start listening on
        voice_data = ""

        try:
            voice_data = c.recognize_google(audio, language='en')  # giọng nói nhận diện sẽ là tiếng anh

        except sr.UnknownValueError:  # bắt lỗi không nhận diện được giọng nói
            speak("Sorry, I did not get that.")
            voice_data = command()
            pass

        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            pass

        return voice_data  # trả về mệnh lệnh của người nói ở dạng text


def speak(text):  # máy sẽ đọc chữ đầu vào
    ann.say(text)  # đọc chữ
    ann.runAndWait()  # chạy và đợi


def measure():
    raw_data = []
    flag = True

    timeout = None

    while flag:
        data_from_sensor = read_sensor()
        if 'No finger' in data_from_sensor:
            raw_data.clear()
            timeout = None
            # print('Please put your finger on the sensor')

        elif data_from_sensor.__len__() == 0:
            continue
        else:
            if timeout is None:
                timeout = time.time() + 10

            if time.time() > timeout:
                flag = False
            else:
                raw_data.append(data_from_sensor)
                # print(data_from_sensor)

    data = raw_data[raw_data.__len__() - 1]
    array = data.split(",")
    speak("Your heart rate is " + array[array.__len__() - 1])


if __name__ == "__main__":  # chỉ chạy các chức năng có trong file sensor và không chạy trong các file khác
    measure()
