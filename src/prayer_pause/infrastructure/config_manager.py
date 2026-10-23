import json

from prayer_pause.domain.config import Config
from prayer_pause.utils import Utils


class ConfigManager:
    def __init__(self):
        self.config_dir = Utils.get_config_dir() / "prayer-pause"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "prayer-pause.json"

    def load(self, in_dict=False) -> Config | dict[str, int]:
        """To Access config options, dot notate the config option after calling the `load()` method."""
        try:
            raw = json.loads(self.config_file.read_text())
            if in_dict:
                return raw
            return Config.from_dict(raw)

        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            # Get the default config values and save them to the json config file.
            config = Config()
            self.save(config)

        # After saving the default values,
        # there is no point of reading from the file
        # since it has the same default options as the Config object.
        if in_dict:
            return config.to_dict()
        # We return the default config values from the `Config` dataclass.
        return config

    def save(self, config: Config | dict[str, int]):
        self.config_file.write_text(
            json.dumps(
                config.to_dict() if isinstance(config, Config) else config,
                indent=4,
            )
        )

    def set(self, key: str, value: int):
        config: dict[str, int] = self.load(in_dict=True)  # pyright: ignore[reportAssignmentType]
        config.update({key: value})
        self.save(config)
