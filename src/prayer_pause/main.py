from PySide6.QtWidgets import QApplication

from prayer_pause.infrastructure.config_manager import ConfigManager
from prayer_pause.infrastructure.prayerapi import PrayerAPI
from prayer_pause.presentation.app import Tray, Window
from prayer_pause.presentation.locker import Locker
from prayer_pause.services.scheduler_service import SchedulerService
from prayer_pause.utils import Utils


def main():
    api = PrayerAPI()
    prayers = api.get_prayers()
    config_manager = ConfigManager()

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    tray = Tray(lambda: Window(prayers, config_manager))
    tray.show()
    locker = Locker(config_manager)

    def temp(): ...

    scheduler_service = SchedulerService(prayers, config_manager)
    scheduler_service.schedule(
        on_prayer=locker.exc,
        on_notification=temp,
    )

    style = Utils.STYLE_FILE.read_text(encoding="utf-8")
    style = style.replace('url("assets/', f'url("{Utils.ASSETS_DIR.as_posix()}/')
    app.setStyleSheet(style)

    print("Prayer Pause is running.")

    app.exec()


if __name__ == "__main__":
    main()
