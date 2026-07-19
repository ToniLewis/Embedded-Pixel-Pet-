import time
from typing import Callable, List


class ScheduledTask:
    def __init__(self, func: Callable[[], None], interval_seconds: float):
        self.func = func
        self.interval = interval_seconds
        self.next_run_time = time.time() + self.interval


class Scheduler:
    """
    Very simple task scheduler.
    You can register functions to be called every N seconds.
    """

    def __init__(self):
        self.tasks: List[ScheduledTask] = []

    def add_task(self, func: Callable[[], None], interval_seconds: float):
        """
        Register a function to be called every `interval_seconds`.
        """
        self.tasks.append(ScheduledTask(func, interval_seconds))

    def update(self):
        """
        Called every frame from main.py.
        Runs any tasks whose scheduled time has arrived.
        """
        now = time.time()
        for task in self.tasks:
            if now >= task.next_run_time:
                task.func()
                task.next_run_time = now + task.interval
