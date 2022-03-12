class SensorData:
    heart_rate = None
    average_heart_rate = None
    spo2 = None

    # datetime = None

    def __int__(self):
        pass

    def __init__(self, heart_rate=None, average_heart_rate=None, spo2=None):
        self.heart_rate = heart_rate
        self.average_heart_rate = average_heart_rate
        self.spo2 = spo2
        # self.datetime = datetime
