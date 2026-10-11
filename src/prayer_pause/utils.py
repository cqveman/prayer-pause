import os
import platform
from datetime import datetime
from pathlib import Path
from typing import ClassVar


class Utils:
    ROOT_DIR = Path(__file__).parent.parent.parent
    ASSETS_DIR = ROOT_DIR / "assets"

    # Values (in minutes) below correspond to the `Config` dataclass members in order.
    MIN_VALUES: ClassVar = [1, 1, 0]
    MAX_VALUES: ClassVar = [60, 60, 60]

    @classmethod
    def time_to_datetime(cls, time_str: str) -> datetime:
        """Takes a string with the format of `H:M` and returns a full datetime obj with current day with that time string"""
        time_obj = datetime.strptime(time_str, "%H:%M").time()
        parsed_time = datetime.combine(datetime.today().date(), time_obj)

        return parsed_time

    @classmethod
    def to_12h_time(cls, time_24: str):
        """Converts a 24-hour time string (HH:MM) to 12-hour format (I:MM AM/PM)."""
        return datetime.strptime(time_24, "%H:%M").strftime("%I:%M %p").lstrip("0")

    @classmethod
    def get_config_dir(cls) -> Path:
        system = platform.system()

        if system == "Linux":
            xdg_config = os.environ.get("XDG_CONFIG_HOME")
            return Path(xdg_config) if xdg_config else Path.home() / ".config"

        elif system == "Windows":
            appdata = os.environ.get("APPDATA")
            return Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"

        raise ValueError(f"Unsupported platform: {system!r}")

    @classmethod
    def get_cache_dir(cls) -> Path:
        system = platform.system()

        if system == "Linux":
            xdg_cache = os.environ.get("XDG_CACHE_HOME")
            return Path(xdg_cache) if xdg_cache else Path.home() / ".cache"

        elif system == "Windows":
            local_appdata = os.environ.get("LOCALAPPDATA")
            return (
                Path(local_appdata)
                if local_appdata
                else Path.home() / "AppData" / "Local"
            )

        raise ValueError(f"Unsupported platform: {system!r}")

    @classmethod
    def get_display_manager(cls) -> str:
        """Returns if the current session is running X11 or Wayland. On linux only."""
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()

        # fmt: off
        if session_type == "wayland": return "Wayland"
        elif session_type == "x11": return "X11"
        return "Unknown"
        # fmt: on

    @classmethod
    def format_config_key(cls, key: str) -> str:
        suffixes = ["_minutes"]

        for s in suffixes:
            if key.endswith(s):
                key = key.removesuffix(s)
                break
        # Convert `config_option` to `Config Option`
        return key.replace("_", " ").title()
