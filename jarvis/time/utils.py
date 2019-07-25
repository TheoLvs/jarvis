# Standard libraries
import time
import datetime

# Win32 libraries
from win32gui import GetWindowText, GetForegroundWindow
from ctypes import Structure, windll, c_uint, sizeof, byref

def get_active_window():
    return GetWindowText(GetForegroundWindow())


def get_active_application():
    pass

def now(as_str = False):
    if not as_str:
        return time.time()
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today():
    return datetime.datetime.now().strftime('%Y-%m-%d')


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





class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]


def get_idle_time():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0