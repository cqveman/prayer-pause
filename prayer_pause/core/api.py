from datetime import datetime
import requests


def _filter_prayers(data: dict, SKIP, skip_nafl: bool = False):
    prayers = data["data"]["timings"]

    filtered = {}
    for p in prayers:
        if skip_nafl:
            SKIP.extend(('Sunrise', 'Sunset'))
        if p in SKIP:
            continue
        filtered[p] = prayers[p]
    return filtered


def _get_location():
    user_ip = requests.get('https://api.ipquery.io').text

    # 1,000 queries / day
    response = requests.get(f'https://api.ip2location.io/?ip={user_ip}')
    data = response.json()

    city = data.get('city_name')
    country_code = data.get('country_code')

    return city, country_code


def _get_today_date():
    return datetime.today().strftime('%d-%m-%Y')


# TODO: offline prayer times calculation
def get_prayers(skip_nafl=True):
    URL = 'https://api.aladhan.com/v1/timingsByCity'
    SKIP = ['Imsak', 'Midnight', 'Firstthird', 'Lastthird']

    city, country = _get_location()

    params = {
        'date': _get_today_date(),
        'city': city,
        'country': country
    }

    try:
        response = requests.get(URL, params)

    except Exception as e:
        print(f"Could not fetch prayer times ({e}). Try again later.")

    else:
        filtered_data = _filter_prayers(response.json(), SKIP, skip_nafl)
        return filtered_data
