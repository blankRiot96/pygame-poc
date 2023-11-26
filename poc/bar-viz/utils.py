import time


class Time:
    """Class to check if a certain amount of time has passed."""

    def __init__(self, time_to_pass: float):
        self.time_to_pass = time_to_pass
        self.start = time.perf_counter()

    def reset(self) -> None:
        self.start = time.perf_counter()

    def tick(self) -> bool:
        if time.perf_counter() - self.start > self.time_to_pass:
            self.start = time.perf_counter()
            return True
        return False

    def get_time_left(self) -> float:
        return self.time_to_pass - (time.perf_counter() - self.start)
