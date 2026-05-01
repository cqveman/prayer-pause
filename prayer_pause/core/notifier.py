from plyer import notification

from prayer_pause.utils import get_resource_path


def notify(prayer_name: str, minutes: int):
    icon = get_resource_path('app.ico')
    notification.notify(
        title='Adhan Reminder',
        message=f'{minutes} minutes until {prayer_name}.',
        app_name='Prayer Pause',
        app_icon=str(icon)
    )
