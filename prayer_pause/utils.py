from datetime import datetime
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG = BASE_DIR / 'config.json'
LOG = BASE_DIR / 'prayer_pause.log'


def time_to_datetime(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M').time().replace(microsecond=0)
    parsed_time = datetime.combine(datetime.today().date(), time_obj)

    return parsed_time


def load_config():
    try:
        with open(CONFIG) as f:
            config = json.load(f)
        return config['notify_duration_in_minutes'], config['lock_duration_in_minutes']

    except FileNotFoundError:
        raise RuntimeError(f"Config file not found at {CONFIG}.")

    except KeyError as e:
        raise RuntimeError(f"Missing key in config.json: {e}")


def update_config(notify_dur, lock_dur):
    if notify_dur <= 0 or lock_dur <= 0:
        raise ValueError('Duration must be larger than 0 minutes.')

    with open(str(CONFIG), 'w') as f:
        json.dump({
            'notify_duration_in_minutes': notify_dur,
            'lock_duration_in_minutes': lock_dur
        }, f, indent=4)
