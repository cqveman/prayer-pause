import json
from pathlib import Path

from prayer_pause.domain.config import Config


class ConfigManager:
    def __init__(self) -> None:
        self.config_dir = Path()
        self._resolve_config_dir()
        self.file_path = self.config_dir / "prayer-pause.json"

    def _resolve_config_dir(self) -> None:
        import os
        import platform

        if platform.system() == "Linux":
            xdg_config = os.environ.get("XDG_CONFIG_HOME")
            base = Path(xdg_config) if xdg_config else Path.home() / ".config"
            self.config_dir = base / "prayer-pause"

        elif platform.system() == "Windows":
            appdata = os.environ.get("APPDATA")
            base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
            self.config_dir = base / "prayer-pause"

        else:
            raise ValueError(f"Unsupported platform: {platform.system()!r}")

        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_config(self) -> Config:
        try:
            raw = json.loads(self.file_path.read_text())
            return Config.from_dict(raw)

        except (FileNotFoundError, json.JSONDecodeError):  # Use default values
            config = Config()
            self.save_config(config)

        return Config.from_dict(config.to_dict())

    def save_config(self, config: Config) -> None:
        self.file_path.write_text(json.dumps(config.to_dict(), indent=4))
