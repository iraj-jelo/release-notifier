from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger


class SchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def start(self) -> None:
        self.scheduler.start()

    def stop(self) -> None:
        self.scheduler.shutdown(wait=False)

    def add_interval_job(self, func, seconds: int, **kwargs) -> None:
        self.scheduler.add_job(func, IntervalTrigger(seconds=seconds), **kwargs)
