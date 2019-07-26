
import sys
sys.path.append("C:/git/jarvis")

from jarvis.time.tracker import TimeTracker


if __name__ == "__main__":

    tracker = TimeTracker(freq = 5)
    tracker.run()