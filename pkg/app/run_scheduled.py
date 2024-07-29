import schedule
import time
from typing import Callable
from pkg.app.run import run_crawlers
from pkg.config import config


def run_crawlers_scheduled(active: Callable[[], bool] = lambda: True) -> None:
    schedule.every(config.scheduler_seconds).seconds.do(run_crawlers)

    while active():
        schedule.run_pending()
        time.sleep(1)
