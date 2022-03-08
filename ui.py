from tkinter import *


def on_click_speak_button():
    global isListening
    if isListening:
        speakButton.config(image=blueMicIcon)
        isListening = not isListening
    else:
        speakButton.config(image=redMicIcon)
        isListening = not isListening


def on_enter_speak_button(event):
    if not isListening:
        speakButton.config(image=blueMicIcon)


def on_leave_speak_button(event):
    if not isListening:
        speakButton.config(image=blueEdgeMicIcon)


def on_click_ask_entry(event):
    askEntry.configure(state=NORMAL)
    askEntry.delete(0, END)

    # make the callback only work once
    askEntry.unbind('<Button-1>', on_click_ask_entry_id)


def settings():
    pass


def feedback():
    pass


def about():
    pass


def on_click_three_dots_button(event):
    threeDotsMenu.tk_popup(event.x_root, event.y_root)


window = Tk()
window.bind_all("<Button-1>", lambda event: event.widget.focus_set())

isListening = False
blueEdgeMicIcon = PhotoImage(file="icon/blue-edge-mic.png")
blueMicIcon = PhotoImage(file="icon/blue-mic.png")
redMicIcon = PhotoImage(file="icon/voice-wave.png")

window.geometry("390x640")
window.title("Healthcare Virtual Assistant")
windowIcon = PhotoImage(file="icon/logo.png")
window.iconphoto(True, windowIcon)

speakButton = Button(window,
                     image=blueEdgeMicIcon,
                     borderwidth=0,
                     command=on_click_speak_button)
speakButton.place(relx=0.5, rely=1.0, y=-50, anchor=S)
speakButton.bind("<Enter>", on_enter_speak_button)
speakButton.bind("<Leave>", on_leave_speak_button)

askEntry = Entry(window,
                 width=35,
                 bg="#F0F0F0",
                 borderwidth=0,
                 font=("Arial", 13))
askEntry.insert(0, 'Ask me')
askEntry.configure(state=DISABLED)
askEntry.place(relx=0, rely=1.0, anchor=SW, x=10, y=-10)
on_click_ask_entry_id = askEntry.bind('<Button-1>', on_click_ask_entry)

sendIcon = PhotoImage(file="icon/send-outline.png")
sendTextButton = Button(window,
                        image=sendIcon,
                        borderwidth=0)
sendTextButton.place(relx=1, rely=1, anchor=SE, x=-10, y=-6)

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


