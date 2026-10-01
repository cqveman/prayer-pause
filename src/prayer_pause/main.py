from pathlib import Path

from PySide6.QtWidgets import QApplication

from prayer_pause.infrastructure.config_manager import ConfigManager
from prayer_pause.infrastructure.prayerapi import PrayerAPI
from prayer_pause.presentation.app import Tray, Window
from prayer_pause.presentation.locker import Locker
from prayer_pause.services.scheduler_service import SchedulerService


def main():
    api = PrayerAPI()
    prayers = api.get_prayers()
    config_manager = ConfigManager()

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    tray = Tray(lambda: Window(prayers, config_manager))
    tray.show()
    locker = Locker(config_manager)

    scheduler_service = SchedulerService(prayers, config_manager)
    scheduler_service.schedule(
        on_prayer=locker.exc,
        on_notification=lambda n, rm: print(n, rm),
    )

    with open(Path(__file__).parent.parent.parent / "style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    app.exec()


if __name__ == "__main__":
    main()
