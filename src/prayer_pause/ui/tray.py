import pystray
from pystray import MenuItem
from PIL import Image

from prayer_pause.ui.settings import settings_menu
from prayer_pause.utils import get_resource_path


def run_tray(on_settings_saved):
    icon_path = get_resource_path('app.ico')
    icon = pystray.Icon(
        'PrayerPause',
        Image.open(icon_path),
        menu=pystray.Menu(
            MenuItem('Settings', lambda ico, item: settings_menu(on_settings_saved)),
            MenuItem('Quit', lambda ico, item: ico.stop()),
        )
    )
    icon.run()
