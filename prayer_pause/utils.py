import os
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler

# https://beta.stackoverflow.com/q/30218802#30218825
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(BASE_DIR, 'config.json')
LOG = os.path.join(BASE_DIR, 'prayer_pause.log')


def time_to_datetime(time_str):
    time_obj = datetime.strptime(time_str, '%H:%M').time().replace(microsecond=0)
    parsed_time = datetime.combine(datetime.today().date(), time_obj)

    return parsed_time


def load_config():  # TODO: add try-except
    with open(str(CONFIG)) as f:
        config = json.load(f)

    notify_dur = config['notify_duration_in_minutes']
    lock_dur = config['lock_duration_in_minutes']

    return notify_dur, lock_dur


def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(LOG, maxBytes=5 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
