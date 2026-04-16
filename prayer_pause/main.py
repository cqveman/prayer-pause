from prayer_pause.api import get_prayers
from prayer_pause.scheduler import schedule

try:
    prayers = get_prayers()
except Exception:
    prayers = {'Fajr': '08:50', 'Dhuhr': '14:02', 'Asr': '15:36', 'Maghrib': '18:27', 'Isha': '22:39'}
schedule(prayers)
