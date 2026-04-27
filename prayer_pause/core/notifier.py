from plyer import notification

from prayer_pause.utils import BASE_DIR


def notify(prayer_name: str, minutes: int):
    icon = BASE_DIR / 'app.ico'
    notification.notify(
        title='Adhan Reminder',
        message=f'{minutes} minutes until {prayer_name}.',
        app_name='Prayer Pause',
        app_icon=str(icon)
    )
