import time


class Timer:

    def __init__(self):
        self._start = None

    def start(self):
        self._start = time.perf_counter()

    def stop(self):
        return round(
            time.perf_counter() - self._start,
            4
        )