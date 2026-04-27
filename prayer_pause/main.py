import subprocess
import sys
from pathlib import Path

from prayer_pause.core.api import get_prayers
from prayer_pause.core.scheduler import schedule, reload_scheduler
from prayer_pause.ui.locker import settings_menu
from prayer_pause.ui.tray import run_tray


def _run_locker(prayer_name: str, duration_minutes: int):
    locker_path = Path(__file__).parent / 'ui' / 'locker.py'
    try:
        subprocess.Popen([sys.executable, str(locker_path), prayer_name, str(duration_minutes)])
    except Exception as e:
        print(f"Failed to launch locker for {prayer_name}: {e}")


def _reload():
    prayers = get_prayers()
    reload_scheduler(prayers, on_prayer=_run_locker)


def open_settings_menu():
    settings_menu(_reload)


def main():
    prayers = get_prayers()
    # Start background scheduler
    schedule(prayers, on_prayer=_run_locker)
    # Run tray app
    run_tray(on_settings_saved=_reload)

    open_settings_menu()


# TODO: turn the app from a foreground process to a service (systemd), because it can starts automatically on boot in linux.
if __name__ == "__main__":
    main()
