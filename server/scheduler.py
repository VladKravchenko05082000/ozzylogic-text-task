import threading

from controllers.sync.sync_controllers import (
    sync_min_fin_bank_rates, sync_nbu_rates
)
from controllers.sync.banks.controller import (sync_banks, sync_branches)
from configs.general_constants import (RATES_INTERVAL_MINUTES_TIME, BANKS_UPDATE_INTERVAL_HOURS)
from lib.helpers import format_seconds_to_define_unit

from typing import Callable
from configs.types import TimeUnit

class _Scheduler:
    def __init__(self):
        self._stop = threading.Event()
        self._threads: list[threading.Thread] = []

    def _run_job(self, fn: Callable, interval_sec: float) -> None:
        while not self._stop.wait(timeout=interval_sec):
            fn()

    def add_job(self, fn, interval: float, timeType: TimeUnit = "minute") -> None:
        interval_sec = format_seconds_to_define_unit(interval, unit=timeType)
        t = threading.Thread(
            target=self._run_job,
            args=(fn, interval_sec),
            daemon=True,
        )
        self._threads.append(t)
        t.start()

    def shutdown(self, wait: bool = True) -> None:
        self._stop.set()
        if wait:
            for t in self._threads:
                t.join()


def start_scheduler() -> _Scheduler:
    scheduler = _Scheduler()
    scheduler.add_job(sync_min_fin_bank_rates, RATES_INTERVAL_MINUTES_TIME)
    scheduler.add_job(sync_nbu_rates, RATES_INTERVAL_MINUTES_TIME)
    scheduler.add_job(sync_banks, BANKS_UPDATE_INTERVAL_HOURS, timeType="hour")
    scheduler.add_job(sync_branches, BANKS_UPDATE_INTERVAL_HOURS, timeType="hour")
    return scheduler
