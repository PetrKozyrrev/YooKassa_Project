from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import UTC

from .recurrent import recurrent_worker

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(recurrent_worker, "cron", hour=0, timezone=UTC)

    scheduler.start()
    print("Scheduler started")