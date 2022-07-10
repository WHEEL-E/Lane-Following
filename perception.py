import sys
import threading

import landmark_ocr
import lane_follower

class Thread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def kill(self):
        self._stop_event.set()

    def is_killed(self):
        return self._stop_event.is_set()


destination = "bedroom1"

lane_follower_thread = Thread(target=lane_follower.main)
landmark_ocr_thread = Thread(target=landmark_ocr.main, args=(destination,))

try:
    lane_follower_thread.start()
    landmark_ocr_thread.start()

except KeyboardInterrupt:
    lane_follower_thread.kill()
    landmark_ocr_thread.kill()

    sys.exit()
