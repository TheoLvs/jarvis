

# Standard libraries
import os
import time
import logging
import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Win32 libraries
from win32gui import GetWindowText, GetForegroundWindow

"""
Notes:
    - Logging official tutorial https://realpython.com/python-logging/
"""


LOG_DIR = Path(os.path.dirname(__file__)).absolute().parent / "logs"


class TimeTracker:

    def __init__(self,freq = 10,log_dir = LOG_DIR):

        self.freq = freq
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok = True)
        self._init_logger()
        logging.info(">> Starting time tracking session")


    def _init_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s',"%Y-%m-%d %H:%M:%S"
            )
        file_handler = logging.handlers.RotatingFileHandler(self.log_dir / f"{self.today()}_jarvis_time_tracker.log", 'a') #, 1000000, 1)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def run(self,duration = 10*60*60):
        print(f"... Launching time tracking for {self.sec_to_hms(duration)} at {self.now(as_str = True)}")
        s = self.now()
        active_window = self.get_active_window()
        logging.info(active_window)
        while self.now() - s < duration:
            new_active_window = self.get_active_window()
            if new_active_window != active_window:
                logging.info(new_active_window)
                active_window = new_active_window
            time.sleep(self.freq)


    @staticmethod
    def get_active_window():
        return GetWindowText(GetForegroundWindow())


    @staticmethod
    def get_active_application():
        pass

    @staticmethod
    def now(as_str = False):
        if not as_str:
            return time.time()
        else:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    @staticmethod
    def today():
        return datetime.datetime.now().strftime('%Y-%m-%d')


    @staticmethod
    def sec_to_hms(seconds):
        if seconds < 60:
            return "{}s".format(int(seconds))
        elif seconds < 60*60:
            m,s = divmod(int(seconds),60)
            return "{}m{}s".format(m,s)
        else:
            m,s = divmod(int(seconds),60)
            h,m = divmod(m,60)
            return "{}h{}m{}s".format(h,m,s)


    def load(self):
        pass


    def _to_df(self):
        pass


    def show(self):
        pass




if __name__ == "__main__":

    tracker = TimeTracker(freq = 5)
    tracker.run()