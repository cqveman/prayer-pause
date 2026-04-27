from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from prayer_pause.core.notifier import notify
from prayer_pause.utils import time_to_datetime, load_config

scheduler = BackgroundScheduler()


def schedule(prayers: dict, on_prayer):
    """Takes a prayers dict {prayer_name: 'HH:MM'}, and a callable function passed by `main.py`"""
    current_time = datetime.now()
    notify_mins, lock_mins = load_config()

    for name, time_str in prayers.items():
        prayer_datetime = time_to_datetime(time_str)
        notify_time = prayer_datetime - timedelta(minutes=notify_mins)

        # Skip prayer if it was in the past
        if prayer_datetime < current_time:
            continue

        # Schedule notifier IF the current time is still hasn't come (we are still in the past)
        if notify_time > current_time:
            print(f"Scheduled notifier for {name} at {notify_time.time()}")
            scheduler.add_job(
                func=notify,
                args=[name, notify_mins],
                trigger='date',
                run_date=notify_time,
            )

        print(f"Scheduled locker for {name} at {prayer_datetime.time()}")
        scheduler.add_job(
            func=on_prayer,
            args=[name, lock_mins],
            trigger='date',
            run_date=prayer_datetime,
        )

    # Only start the scheduler if it's not running before
    if scheduler.state == 0:
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("Scheduler stopped by user.")

def reload_scheduler(prayers, on_prayer):
    scheduler.remove_all_jobs()
    schedule(prayers, on_prayer)
