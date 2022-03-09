import serial  # cài đặt thư viện
import pttxy3

ArduinoSerial = serial.Serial('COM3', 115200)  # Khởi tạo cổng mà kết nối tới Adruino


# Parameters:
# port: tên cổng nối với arduino
# baudrate: tốc độ baud ví dụ như 9600 hoạch 11520


# def LED(data):
#     if 'On' in data:
#         ArduinoSerial.write(b'')
#     elif 'Off' in data:
#         ArduinoSerial.write(b'')


# while True:
#     print("Type 'On' to turn on the LED and type 'Off to turn off the LED'")
#     data = input("")
#     LED(data)

def ReadSensor():
    if ArduinoSerial.inWaiting() > 0:
        ArduinoSerial.write(13)
        myData = ArduinoSerial.readline()
        print(myData)
        # if 'MAX30102 was not found' in myData:
        #     # speak('MAX30102 was not found. Please check wiring/power.')
        #     print('MAX30102 was not found. Please check wiring/power.')
        # elif 'finger' in myData:
        #     # speak('Place your index finger on the sensor with steady pressure.')
        #     print('Place your index finger on the sensor with steady pressure.')


while True:
    ReadSensor()

# while True:
#     if ArduinoSerial.inWaiting() > 0:
#         myData = ArduinoSerial.readline();
#         print(myData);
