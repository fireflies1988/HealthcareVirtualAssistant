class Reminder:
    memo = None
    time = None
    date = None
    is_repeated = None

    def __init__(self):
        pass

    def __int__(self, memo, date, time, is_repeated):
        self.memo = memo
        self.time = time
        self.date = date
        self.is_repeated = is_repeated


