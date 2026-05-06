import os
import sys
from datetime import datetime
import json
from pathlib import Path

DEFAULTS = {
    'notify_duration_in_minutes': 10,
    'lock_duration_in_minutes': 20,
    'locker_offset_in_minutes': 0,
    'before_or_after': 'NONE'
}


def get_resource_path(filename: str, is_config=False):
    if getattr(sys, 'frozen', False):
        # If it's a config file then set create it at `C:\Users\tryme\AppData\Roaming` (for Windows)
        if is_config:
            base_path = Path(os.getenv('APPDATA')) / 'PrayerPause'
            base_path.mkdir(exist_ok=True)
            return base_path / filename

        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent.resolve()
    # Returns full absolute path
    return base_path.joinpath(filename)


def time_to_datetime(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M').time().replace(microsecond=0)
    parsed_time = datetime.combine(datetime.today().date(), time_obj)

    return parsed_time


CONFIG = get_resource_path('config.json', is_config=True)


def load_config():
    try:
        with open(CONFIG) as f:
            config = json.load(f)

        notify_dur = config['notify_duration_in_minutes']
        lock_dur = config['lock_duration_in_minutes']
        locker_offset = config['locker_offset_in_minutes']
        before_or_after = config['before_or_after']

        return notify_dur, lock_dur, locker_offset, before_or_after

    except FileNotFoundError:
        print(f"Missing config file. Creating a new one.")

        with open(CONFIG, 'w') as f:
            json.dump(DEFAULTS, f, indent=4)

        load_config()

    except KeyError as e:
        raise RuntimeError(f"Missing key in config.json: {e}")


def update_config(notify_dur, lock_dur, locker_offset, before_or_after):
    if notify_dur <= 0 or lock_dur <= 0:
        raise ValueError('Value must be larger than 0 minutes.')

    if locker_offset < 0:
        raise ValueError('Offset can\'t be a negative value.')

    with open(CONFIG, 'w') as f:
        json.dump({
            'notify_duration_in_minutes': notify_dur,
            'lock_duration_in_minutes': lock_dur,
            'locker_offset_in_minutes': locker_offset,
            'before_or_after': before_or_after
        }, f, indent=4)
