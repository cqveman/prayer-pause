from datetime import datetime
import requests

class AlAdhan():
    def __init__(self):
        self.user_ip = requests.get('https://api.ipquery.io').text
        self.url = "https://api.aladhan.com/v1/timingsByCity" 
        self.nafl_prayers = ['Sunrise', 'Sunset', 'Imsak', 'Midnight', 'Firstthird', 'Lastthird']

    def _filter_prayers(self, data: dict):
        prayers = data["data"]["timings"]

        filtered = {}
        for p in prayers:
            if p in self.nafl_prayers:
                continue
            filtered[p] = prayers[p]

        return filtered

    def get_current_date(self):
        return datetime.today().strftime('%d-%m-%Y')

    def get_user_location(self):
        # 1,000 queries / day
        response = requests.get(f'https://api.ip2location.io/?ip={self.user_ip}')
        data = response.json()

        city = data.get('city_name')
        country_code = data.get('country_code')

        return city, country_code

    def get_prayers(self):
        city, country = self.get_user_location()

        params = {
                'date': self.get_current_date(),
                'city': city,
                'country': country
                }

        try:
            response = requests.get(self.url, params=params).json()
        except Exception as e:
            print(f"Could not fetch prayer times ({e}). Try again later.")
        else:
            filtered_data = self._filter_prayers(response)
            return filtered_data
