import multiprocessing
from multiprocessing import Process

from prayer_pause.core.api import get_prayers
from prayer_pause.core.notifier import notify_startup
from prayer_pause.core.scheduler import schedule_prayers, reload_scheduler
from prayer_pause.ui.locker import lock
from prayer_pause.ui.tray import run_tray


def _run_locker(prayer_name: str, duration_minutes: int):
    try:
        p = Process(target=lock, args=[prayer_name, duration_minutes], daemon=False)
        p.start()
    except Exception as e:
        print(f"Failed to launch locker for {prayer_name}: {e}")


def _reload():
    prayers = get_prayers()
    reload_scheduler(prayers, on_prayer=_run_locker)


def main():
    multiprocessing.freeze_support()  # Used by pyinstaller
    prayers = get_prayers()
    # Start background scheduler
    notify_startup()
    schedule_prayers(prayers, on_prayer=_run_locker)
    print()
    # Run tray app
    run_tray(on_settings_saved=_reload)


if __name__ == "__main__":
    main()
