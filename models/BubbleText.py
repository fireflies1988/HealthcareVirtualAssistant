import tkinter


class BubbleText:
    x = None
    y = None
    relx = None
    rely = None
    text = None

    def __int__(self):
        pass

    def __init__(self, x, y, relx, rely, text):
        self.x = x
        self.y = y
        self.relx = relx
        self.rely = rely
        self.text = text

    # def place(self, window):
    #     window.place(relx=self.relx, rely=self.rely, x=self.x, y=self.y)
