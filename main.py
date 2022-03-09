from ui import *
from virtual_assistant import *

if __name__ == "__main__":
    window.after(500, introduce)    # after mainloop() 500ms, call introduce()
    window.mainloop()

# speak("Hi, say something...")
# while 1:
#     data = record_audio()
#     respond(data)
