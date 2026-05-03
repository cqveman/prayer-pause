from plyer import notification

from prayer_pause.utils import get_resource_path

icon = get_resource_path('app.ico')


def notify_startup():
    notification.notify(
        title='Prayer Pause',
        message='App is running in the background.',
        app_icon=str(icon),
        timeout=4,
    )


def notify_adhan(prayer_name: str, minutes: int):
    notification.notify(
        title='Adhan Reminder',
        message=f'{minutes} minutes until {prayer_name}.',
        app_name='Prayer Pause',
        app_icon=str(icon)
    )
