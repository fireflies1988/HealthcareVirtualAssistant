import tkinter
from tkinter import *

import ui
from virtual_assistant import *

import threading
import BubbleText

global command
command = ""


#
# threading
#
def change_speak_button_status():
    speakButton.config(image=voiceWaveIcon)


def listen():
    playsound.playsound('sound/data_2.wav')
    global isListening
    global command
    try:
        command = record_audio()
        respond(command)
        isListening = not isListening
        speakButton.config(image=blueEdgeMicIcon)
    except sr.UnknownValueError:
        isListening = not isListening
        speakButton.config(image=blueEdgeMicIcon)
    except sr.RequestError:
        isListening = not isListening
        speakButton.config(image=blueEdgeMicIcon)


#
# UI EVENT HANDLERS
#
def on_click_speak_button():
    heart_button.place(relx=-1.0, rely=-1.0, anchor=N)
    # heart_rate_label.place(relx=-1.0, rely=-1.0, anchor=N)
    # spo2_label.place(relx=-1.0, rely=-1.0, anchor=N)
    # measure_label.place(relx=-1.0, rely=-1.0, anchor=N)
    # warning_label.place(relx=-1.0, rely=-1.0, anchor=N)
    measure_label.place_forget()
    warning_label.place_forget()
    heart_rate_label.place_forget()
    spo2_label.place_forget()



    global command
    global isListening
    if not isListening:
        isListening = not isListening
        # threading.Thread(target=change_speak_button_status).start()
        change_speak_button_status()
        threading.Thread(target=listen).start()


def on_enter_speak_button(event):
    if not isListening:
        speakButton.config(image=blueMicIcon)


def on_leave_speak_button(event):
    if not isListening:
        speakButton.config(image=blueEdgeMicIcon)


def on_click_ask_entry(event):  # textfield function
    askEntry.configure(state=NORMAL)
    askEntry.delete(0, END)  # delete string in textfield


def on_focus_out_ask_entry(event):
    askEntry.delete(0, END)
    askEntry.insert(0, 'Ask me')
    askEntry.configure(state=DISABLED)
    window.focus()


def on_enter_send_button(event):
    sendTextButton.config(image=sendIcon)


def on_leave_send_button(event):
    sendTextButton.config(image=sendOutlineIcon)


def settings():
    pass


def feedback():
    pass


def about():
    pass


def on_click_three_dots_button(event):
    threeDotsMenu.tk_popup(event.x_root, event.y_root)


#
# UI Design
#
window = Tk()
window.bind_all("<Button-1>", lambda event: event.widget.focus_set())  #

# variables #initialize the icons
isListening = False
blueEdgeMicIcon = PhotoImage(file="icon/blue-edge-mic.png")
blueMicIcon = PhotoImage(file="icon/blue-mic.png")
voiceWaveIcon = PhotoImage(file="icon/voice-wave.png")
heartIcon = PhotoImage(file="icon/heart.png")

# window
window.geometry("390x640")
window.title("Healthcare Virtual Assistant")
windowIcon = PhotoImage(file="icon/logo.png")
window.iconphoto(True, windowIcon)

# speak button
speakButton = Button(window,
                     image=blueEdgeMicIcon,
                     borderwidth=0,
                     command=on_click_speak_button)
speakButton.place(relx=0.5, rely=1.0, y=-50, anchor=S)
speakButton.bind("<Enter>", on_enter_speak_button)
speakButton.bind("<Leave>", on_leave_speak_button)

# heart icon
heart_button = Button(window,
                      image=heartIcon,
                      borderwidth=0)
# heart_button.place(relx=0.5, rely=0.0, y=50, anchor=N)


heart_rate_label = Label(window, text="Your heart rate is")
# heart_rate_label.place(relx=0.5, rely=0.0, anchor=N, y=120)
spo2_label = Label(window, text="Your spo2 is")
# spo2_label.place(relx=0.5, rely=0.0, anchor=N, y=140)
measure_label = Label(ui.window, text=f"Measuring...", font=("Roboto", 14), padx=10)
warning_label = Label(ui.window, text=f"Place your index finger on sensor", font=("Roboto", 14), padx=10)


# BubleText
# bubble_text = BubbleText(10, None, 0.0, 0.0, "Hi, I'm your healthcare virtual assistant. What can I do for you?")
# new_label = Label(window, text="Hi, I'm your healthcare virtual assistant. What can I do for you?")


# Textfield "Ask me"
askEntry = Entry(window,
                 width=35,
                 bg="#F0F0F0",
                 borderwidth=0,
                 font=("Arial", 13))
askEntry.place(relx=0, rely=1.0, anchor=SW, x=10, y=-10)
askEntry.insert(0, 'Ask me')
askEntry.configure(state=DISABLED)
askEntry.bind('<Button-1>', on_click_ask_entry)
askEntry.bind("<FocusOut>", on_focus_out_ask_entry)

# send button
sendOutlineIcon = PhotoImage(file="icon/send-outline.png")
sendIcon = PhotoImage(file="icon/send.png")
sendTextButton = Button(window,
                        image=sendOutlineIcon,
                        borderwidth=0)
sendTextButton.bind("<Enter>", on_enter_send_button)
sendTextButton.bind("<Leave>", on_leave_send_button)
sendTextButton.place(relx=1, rely=1, anchor=SE, x=-10, y=-6)

# three-dot menu
threeDotsMenu = Menu(window, tearoff=False)
threeDotsMenu.add_command(label="Settings", command=settings)
threeDotsMenu.add_command(label="Feedback", command=feedback)
threeDotsMenu.add_command(label="About", command=about)
threeDotsIcon = PhotoImage(file="icon/dots.png")
threeDotsButton = Button(window,
                         image=threeDotsIcon,
                         borderwidth=0)
threeDotsButton.bind("<Button-1>", on_click_three_dots_button)
threeDotsButton.place(relx=0, rely=0, x=10, y=10)
