
# Standard libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Custom libraries
from .utils import today,now

LOG_DIR = Path(os.path.dirname(__file__)).absolute().parent.parent / "logs"


class Activity:
    def __init__(self,filepath = None,log_dir = LOG_DIR,freq = 30):

        self.freq = freq
        self.filepath = self._find_file(filepath,log_dir)
        self._read_file()
        self._parse_file()


    def _find_file(self,filepath,log_dir):
        if filepath is None:
            files = os.listdir(log_dir)
            today_str = today()
            filepath = [file for file in files if file.startswith(today_str)][0]
        filepath = Path(log_dir) / Path(filepath)
        assert filepath.exists()
        return filepath


    def _read_file(self):

        # Constants
        sep = " :: "
        start_line = self.filepath.name[:4] # Get year of the file

        # Read file and parse lines
        self.data = open(self.filepath,"r")
        self.data = [line.split(sep) for line in self.data if line.startswith(start_line)]


    def _parse_file(self):

        self.data = (pd.DataFrame(self.data,columns = ["start_time","log_level","window"])
            .assign(start_time = lambda x : pd.to_datetime(x["start_time"]))
            .query("log_level=='INFO'").drop(columns = "log_level")
            .assign(end_time = lambda x : x["start_time"].shift(-1))
            .assign(duration = lambda x : x["end_time"]-x["start_time"])
        )
        self.data = pd.concat([
            self.data.drop(columns = "window"),
            self.data["window"]
                .str.strip()
                .str.rsplit(" - ",1)
                .apply(pd.Series)
                .rename(columns = {0:"window",1:"application"})
        ],axis = 1)



    def show_application_usage(self):
        self.data.groupby("application")["duration"].sum().sort_values().plot(kind = "barh")
        plt.show()


    def watch_last_logs(self,hours = 0,minutes = 0,seconds = 0):
        return self.data.loc[self.data["start_time"] > self.data.iloc[-1]["start_time"] - pd.DateOffset(hours = hours,minutes = minutes,seconds = seconds)]


    def was_idle_in_the_last(self,**kwargs):
        return len(self.watch_last_logs(**kwargs).query("window=='IDLE'")) > 0

