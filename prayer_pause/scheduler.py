import os
import subprocess
import sys

from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from prayer_pause.notifier import notify
from prayer_pause.utils import time_to_datetime, load_config, get_logger, BASE_DIR

scheduler = BlockingScheduler()
NOTIFY_DURATION_IN_MINUTES, LOCK_DURATION_IN_MINUTES = load_config()
logger = get_logger('Scheduler')


def run_locker(prayer_name, duration_minutes):
    try:
        subprocess.Popen([sys.executable, os.path.join(BASE_DIR, 'prayer_pause', 'locker.py'), prayer_name, str(duration_minutes)])
    except Exception as e:
        logger.warning(f"Failed to launch locker process: {e}")


def schedule(prayers: dict):
    current_time = datetime.now()
    for name, time_str in prayers.items():

        prayer_datetime = time_to_datetime(time_str)
        notify_time = prayer_datetime - timedelta(minutes=NOTIFY_DURATION_IN_MINUTES)

        # Skip prayer if it was in the past
        if prayer_datetime < current_time:
            continue

        # Schedule notifier IF the current time is still hasn't come (we are still in the past)
        if notify_time > current_time:
            logger.info(f"Scheduled notifier for {name} at {notify_time.time()}")
            scheduler.add_job(
                func=notify,
                args=[name, NOTIFY_DURATION_IN_MINUTES],
                trigger='date',
                run_date=notify_time,
            )

        logger.info(f"Scheduled locker for {name} at {prayer_datetime.time()}")
        scheduler.add_job(
            func=run_locker,
            args=[name, LOCK_DURATION_IN_MINUTES],
            trigger='date',
            run_date=prayer_datetime,
        )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")
