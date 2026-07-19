import time


class Watchdog:
    """
    Simple watchdog timer.

    main.py should call tick() every frame.
    If is_stalled() ever returns True, you could log or
    attempt a soft reset.
    """

    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout_seconds = timeout_seconds
        self.last_tick = time.time()

    def tick(self):
        self.last_tick = time.time()

    def is_stalled(self) -> bool:
        return (time.time() - self.last_tick) > self.timeout_seconds