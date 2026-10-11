import json
from datetime import date, datetime, timedelta

import requests

from prayer_pause.utils import Utils

NAFL_PRAYERS = [
    "Sunrise",
    "Sunset",
    "Imsak",
    "Midnight",
    "Firstthird",
    "Lastthird",
]


class PrayerAPI:
    def __init__(self):
        self.cache_dir = Utils.get_cache_dir() / "prayer-pause"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "prayer_times.json"

    def _filter_prayers(self, data: dict[str, dict]) -> dict[str, str]:
        prayers = data["data"]["timings"]

        filtered = {}
        for p in prayers:
            if p not in NAFL_PRAYERS:
                filtered[p] = prayers[p]

        return filtered

    def _get_current_date(self, cache_days) -> str | list[str]:
        if cache_days > 1:
            # Return the next `self.cache_days` days in the format: DD-MM-YYYY
            return [
                (date.today() + timedelta(days=d)).strftime("%d-%m-%Y")
                for d in range(cache_days)
            ]

        return date.today().strftime("%d-%m-%Y")

    def _get_user_location(self) -> tuple[str, str]:
        user_ip = requests.get("https://api.ipquery.io").text
        location_info = requests.get(f"https://api.ip2location.io/?ip={user_ip}")

        data = location_info.json()

        city = data.get("city_name")
        country_code = data.get("country_code")

        return city, country_code

    def get_prayers(
        self,
        *,
        update: bool = False,
        cache_days: int = 30,
    ) -> dict[str, dict[str, str]]:
        """`cache_days` has no effect if `update` is false."""
        data = {}

        if not update:
            try:
                data = json.loads(self.cache_file.read_text())
                print("Fetched data from local cache.")
            except (FileNotFoundError, json.JSONDecodeError):
                print("No local cache found.")

        # Drop prayer times for days that have already passed,
        # if cache is empty data == {}.
        data = {
            d: times
            for d, times in data.items()
            if datetime.strptime(d, "%d-%m-%Y").date() >= date.today()
        }

        # Fetch times only if:
        #   - data is empty (i.e. {})
        #   - days left in cache are fewer than a week
        #   - `update` was set to true
        if len(data) < 7:
            print("Fetching new prayer times... (Creating local cache)")

            city, country = self._get_user_location()
            dates = self._get_current_date(cache_days)
            # If prayer times were called for the currnet day ONLY
            # then turn it into a list to be loop-able.
            if isinstance(dates, str):
                dates = [dates]

            for d in dates:
                url: str = f"https://api.aladhan.com/v1/timingsByCity/{d}"
                params = {"city": city, "country": country}

                response = requests.get(url, params=params)
                response.raise_for_status()
                data[d] = self._filter_prayers(response.json())

            self.cache_file.write_text(json.dumps(data, indent=4))
            print("Local cache created!")

        return data
