

import win32api
import win32com.client as wincl
from .time import TimeTracker

class Jarvis:
    def __init__(self):
        self.tracker = TimeTracker()
        self.tts = wincl.Dispatch("SAPI.SpVoice")

    def speak(self,message):
        self.tts.Speak(message)


    def alert_box(self,message):
        win32api.MessageBox(0, message, 'Jarvis', 0x00001000) 


    def run_tracker(self):
        self.tracker.run()
