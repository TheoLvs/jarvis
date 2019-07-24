


import time
import logging
from pathlib import Path

logging.warning('Admin logged out')


class TimeTracker:

    def __init__(self,freq = 10,log_dir = None):

        self.freq = freq
        self.log_dir = log_dir
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')



    def run(self):
        import time
        s = time.time()
        while time.time() - s < 30:
            print(GetWindowText(GetForegroundWindow()))
            time.sleep(2)


    def load(self):
        pass


    def _to_df(self):
        pass


    def show(self):
        pass