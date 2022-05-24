import pickle


class Company(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Alarm(object):
    def __init__(self, uuid, hour, minute, message, is_once):
        self.uuid = uuid
        self.hour = hour
        self.minute = minute
        self.is_once = is_once
        self.message = message

    def __get_time__(self):
        return str(self.hour) + ":" + str(self.minute)


def writeFile(alarm_list):
    # alarm_list = []
    # alarm1 = Alarm(1, 5, "hello1", True)
    # alarm2 = Alarm(2, 6, "hello2", True)
    # alarm3 = Alarm(3, 7, "hello3", True)
    # alarm4 = Alarm(4, 8, "hello4", True)
    # alarm5 = Alarm(5, 9, "hello5", True)
    # alarm_list.append(alarm1)
    # alarm_list.append(alarm2)
    # alarm_list.append(alarm3)
    # alarm_list.append(alarm4)
    # alarm_list.append(alarm5)
    with open('alarm_data.pkl', 'wb') as outp:
        pickle.dump(alarm_list, outp, pickle.HIGHEST_PROTOCOL)


def readFile():
    with open('alarm_data.pkl', 'rb') as inp:
        alarm_list = pickle.load(inp)
        return alarm_list


if __name__ == '__main__':
    writeFile([])
    readFile()
