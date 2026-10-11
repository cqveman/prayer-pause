from collections.abc import Callable
from datetime import date, datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from PySide6.QtCore import QObject, Signal

from prayer_pause.infrastructure.config_manager import ConfigManager
from prayer_pause.utils import Utils


class SchedulerService(QObject):
    prayer_signal = Signal(str)
    notification_signal = Signal()

    def __init__(self, prayers: dict[str, dict[str, str]], config_manager: ConfigManager):  # fmt:skip
        super().__init__()

        self._scheduler = BackgroundScheduler()
        self.prayers = prayers
        self.config = config_manager.load()

    def schedule(
        self,
        on_prayer: Callable[[str], None],
        on_notification: Callable[[],],
    ):
        self.prayer_signal.connect(on_prayer)
        self.notification_signal.connect(on_notification)

        self._schedule_day()
        # re-schedule every midnight
        self._scheduler.add_job(
            func=self._rollover,
            trigger="cron",
            hour=0,
            minute=0,
            second=5,
            id="rollover",
            replace_existing=True,
        )
        self._run_scheduler()

    def _rollover(self):
        self._schedule_day()

    def _schedule_day(self):
        day = date.today().strftime("%d-%m-%Y")
        now = datetime.now()

        for name, time_str in self.prayers[day].items():
            prayer_dt = Utils().time_to_datetime(time_str)
            notification_dt = prayer_dt - timedelta(minutes=self.config.prayer_reminder_minutes)  # fmt:skip

            if prayer_dt > now:
                if notification_dt > now:
                    self._scheduler.add_job(
                        func=self.notification_signal.emit,
                        args=[name, self.config.prayer_reminder_minutes],
                        trigger="date",
                        run_date=notification_dt,
                        id=f"{day}-{name}-notify",
                        replace_existing=True,
                    )

                self._scheduler.add_job(
                    func=self.prayer_signal.emit,
                    args=[name],
                    trigger="date",
                    run_date=prayer_dt,
                    id=f"{day}-{name}",
                    replace_existing=True,
                )

    def _run_scheduler(self):
        # Only start the scheduler if it's not running before
        if self._scheduler.state == 0:
            self._scheduler.start()
