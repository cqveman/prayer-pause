from datetime import datetime

import requests


class PrayerAPI:
    def __init__(self):
        self.user_ip = requests.get("https://api.ipquery.io").text
        self.url: str = "https://api.aladhan.com/v1/timingsByCity"
        self.nafl_prayers: list[str] = [
            "Sunrise",
            "Sunset",
            "Imsak",
            "Midnight",
            "Firstthird",
            "Lastthird",
        ]

    def _filter_prayers(self, data: dict[str, dict]) -> dict[str, str]:
        prayers = data["data"]["timings"]

        filtered = {}
        for p in prayers:
            if p in self.nafl_prayers:
                continue
            filtered[p] = prayers[p]

        return filtered

    def _get_current_date(self) -> str:
        return datetime.today().strftime("%d-%m-%Y")

    def _get_user_location(self) -> tuple[str, str]:
        # 1,000 queries / day
        response = requests.get(f"https://api.ip2location.io/?ip={self.user_ip}")
        data = response.json()

        city = data.get("city_name")
        country_code = data.get("country_code")

        return city, country_code

    def get_prayers(self) -> dict[str, str]:
        city, country = self._get_user_location()

        params = {"date": self._get_current_date(), "city": city, "country": country}

        try:
            response = requests.get(self.url, params=params).json()
        except Exception as e:
            print(f"Could not fetch prayer times ({e}). Try again later.")
        else:
            filtered_data = self._filter_prayers(response)

        return filtered_data  # pyright: ignore[reportPossiblyUnboundVariable]
