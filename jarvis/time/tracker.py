

# Standard libraries
import os
import time
import logging
import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Custom libraries
from ..utils import today,sec_to_hms,now,get_active_window,get_idle_time


"""
Notes:
    - Logging official tutorial https://realpython.com/python-logging/
"""


LOG_DIR = Path(os.path.dirname(__file__)).absolute().parent.parent / "logs"


class TimeTracker:

    def __init__(self,freq = 10,max_idle_time = 2*60,log_dir = LOG_DIR):

        self.freq = freq
        self.max_idle_time = max_idle_time
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok = True)
        self._init_logger()

    def _init_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s',"%Y-%m-%d %H:%M:%S")
        file_handler = logging.handlers.RotatingFileHandler(self.log_dir / f"{today()}_jarvis_time_tracker.log", 'a') #, 1000000, 1)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def run(self,duration = 10*60*60):
        logging.info(">> Starting time tracking session")
        print(f"... Launching time tracking for {sec_to_hms(duration)} at {now(as_str = True)}")
        s = now()
        active_window = get_active_window()
        logging.info(active_window)
        idle = False
        while now() - s < duration:
            if not idle:
                new_active_window = get_active_window()
                if new_active_window != active_window:
                    logging.info(new_active_window)
                    active_window = new_active_window
                elif get_idle_time() > self.max_idle_time:
                    new_active_window = "IDLE"
                    logging.info(new_active_window)
                    active_window = new_active_window
                    idle = True
                else:
                    pass

            else:
                if get_idle_time() < self.max_idle_time:
                    idle = False

            time.sleep(self.freq)




if __name__ == "__main__":

    tracker = TimeTracker(freq = 5)
    tracker.run()