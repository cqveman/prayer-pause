from collections.abc import Callable
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from PySide6.QtCore import QObject, Signal

from prayer_pause.infrastructure.config_manager import ConfigManager
from prayer_pause.utils import Utils


class SchedulerService(QObject):
    prayer_signal = Signal(str)

    def __init__(self, prayers: dict[str, str], config_manager: ConfigManager):
        super().__init__()

        self._scheduler = BackgroundScheduler()
        self.prayers = prayers
        self.config_manager = config_manager
        self.config = self.config_manager.load()

    def schedule(self, on_prayer: Callable[[str], None], on_notification: Callable):
        self.prayer_signal.connect(on_prayer)

        for name, time_str in self.prayers.items():
            prayer_datetime = Utils().time_to_datetime(time_str)
            notification_datetime = prayer_datetime - timedelta(
                minutes=self.config.prayer_reminder_minutes  # pyright: ignore[reportAttributeAccessIssue]
            )

            if prayer_datetime > datetime.now():
                if notification_datetime > datetime.now():
                    self._scheduler.add_job(
                        func=on_notification,
                        args=[name, self.config.prayer_reminder_minutes],  # pyright: ignore[reportAttributeAccessIssue]
                        trigger="date",
                        run_date=notification_datetime,
                    )

                self._scheduler.add_job(
                    func=self.prayer_signal.emit,
                    args=[name],
                    trigger="date",
                    run_date=prayer_datetime,
                )

        self._run_scheduler()

    def _run_scheduler(self):
        # Only start the scheduler if it's not running before
        if self._scheduler.state == 0:
            self._scheduler.start()
