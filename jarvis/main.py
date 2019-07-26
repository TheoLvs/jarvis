
import time
import win32api
import win32com.client as wincl
from .time.tracker import TimeTracker
from .time.activity import Activity
from .utils import now

class Jarvis:
    def __init__(self):
        self.tracker = TimeTracker()
        self.activity = Activity()
        self.tts = wincl.Dispatch("SAPI.SpVoice")

    def speak(self,message):
        self.tts.Speak(message)


    def alert_box(self,message):
        win32api.MessageBox(0, message, 'Jarvis', 0x00001000) 


    def run_tracker(self):
        self.tracker.run()


    def run(self,duration = 10*60*60):

        s = now()
        while now() - s < duration:

            if not self.activity.was_idle_in_the_last(hours = 2):
                self.speak("Tu devrais prendre une pause, ça fait deux heures que tu travailles.")

            time.sleep(self.activity.freq)

