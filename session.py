# session.py
import time

SESSION_TIMEOUT = 5 * 60 

class Session:
    def __init__(self):
        self.active = False
        self.last_activity = None

    def start(self):
        self.active = True
        self.last_activity = time.time()

    def touch(self):
        if self.active:
            self.last_activity = time.time()

    def is_expired(self) -> bool:
        if not self.active or self.last_activity is None:
            return True
        return (time.time() - self.last_activity) > SESSION_TIMEOUT

    def remaining_time(self) -> int:
        if not self.active or self.last_activity is None:
            return 0
        remaining = SESSION_TIMEOUT - (time.time() - self.last_activity)
        return max(0, int(remaining))

    def end(self):
        self.active = False
        self.last_activity = None
