from plyer import notification


def notify(prayer_name: str, minutes: int):
    notification.notify(
        title='Adhan Reminder',
        message=f'{minutes} minutes until {prayer_name}.',
        app_name='Prayer Pause'
    )
