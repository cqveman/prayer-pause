import multiprocessing
import sys
import winreg
from multiprocessing import Process
from pathlib import Path

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


def _auto_startup():
    """https://github.com/orgs/community/discussions/156548"""

    def get_exe_path():
        """https://pyinstaller.org/en/stable/runtime-information.html#using-sys-executable-and-sys-argv-0"""
        if getattr(sys, 'frozen', False):
            exe_path = sys.executable
        else:
            base_dir = Path(__file__).parent.parent.parent.resolve()
            exe_path = base_dir / 'dist' / 'prayer-pause.exe'
        return exe_path

    key = winreg.HKEY_CURRENT_USER
    sub_key = r'Software\Microsoft\Windows\CurrentVersion\Run'

    opened_key = winreg.OpenKey(key, sub_key, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(opened_key, 'PrayerPause', 0, winreg.REG_SZ, str(get_exe_path()))
    winreg.CloseKey(opened_key)

    print('~ Added to registry')


def main():
    multiprocessing.freeze_support()  # Used by pyinstaller
    _auto_startup()
    prayers = get_prayers()
    # Start background scheduler
    notify_startup()
    schedule_prayers(prayers, on_prayer=_run_locker)
    print()
    # Run tray app
    run_tray(on_settings_saved=_reload)


if __name__ == "__main__":
    main()
