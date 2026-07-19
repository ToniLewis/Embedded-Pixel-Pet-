import time
from typing import Callable, List


class ScheduledTask:
    def __init__(self, func: Callable, interval_seconds: float):
        self.func = func
        self.interval_seconds = interval_seconds
        self.next_run = time.time() + interval_seconds


class Scheduler:
    def __init__(self):
        self.tasks: List[ScheduledTask] = []

    def add_task(self, func: Callable, interval_seconds: float):
        task = ScheduledTask(func, interval_seconds)
        self.tasks.append(task)

    def run_pending(self):
        now = time.time()
        for task in self.tasks:
            if now >= task.next_run:
                task.func()
                task.next_run = now + task.interval_seconds