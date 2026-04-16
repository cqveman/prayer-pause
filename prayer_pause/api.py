from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def prayers_filter(data: dict, SKIP, skip_nafl: bool = False):
    prayers = data["data"]["timings"]

    filtered = {}
    for p in prayers:
        if skip_nafl:
            SKIP.extend(('Sunrise', 'Sunset'))
        if p in SKIP:
            continue
        filtered[p] = prayers[p]
    return filtered


def get_location():
    key = os.getenv("IP_API_KEY")
    if not key:
        raise ValueError("API Key not found! Check your .env file.")

    user_ip = requests.get('https://api.ipquery.io').text

    response = requests.get(f'https://ip-intelligence.abstractapi.com/v1/?api_key={key}&ip_address={user_ip}')
    data = response.json()

    city = data.get('location').get('city')
    country = data.get('location').get('country_code')

    return city, country


def get_today_date():
    return datetime.today().strftime('%d-%m-%Y')


# TODO: offline prayer times calculation
def get_prayers(skip_nafl=True) -> dict:
    URL = 'https://api.aladhan.com/v1/timingsByCity'
    SKIP = ['Imsak', 'Midnight', 'Firstthird', 'Lastthird']

    city, country = get_location()

    params = {
        'date': get_today_date(),
        'city': city,
        'country': country
    }

    response = requests.get(URL, params)

    filtered_data = prayers_filter(response.json(), SKIP, skip_nafl)
    return filtered_data
