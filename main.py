import requests
import argparse


def get_coordinates(api_key, city):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}"

    response = requests.get(url)
    data = response.json()

    if data["total_results"] > 0:
        latitude = data["results"][0]["geometry"]["lat"]
        longitude = data["results"][0]["geometry"]["lng"]
        return latitude, longitude
    else:
        return None


def request_yandex_weather_api(api_key, latitude, longitude):
    headers = {
        'X-Yandex-API-Key': api_key
    }
    url = "https://api.weather.yandex.ru/v2/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "lang": "ru_RU",
        "limit": 7,
        "hours": 0,
        "extra": 1
    }
    response = requests.get(url, params=params, headers=headers)
    weather_data = response.json()
    return weather_data


def print_weather_forecast(weather_data):
    weather_dict = {
        'clear': 'ясно',
        'partly-cloudy': 'малооблачно',
        'cloudy': 'облачно с прояснениями',
        'overcast': 'пасмурно',
        'drizzle': 'морось',
        'light-rain': 'небольшой дождь',
        'rain': 'дождь',
        'moderate-rain': 'умеренно сильный дождь',
        'heavy-rain': 'сильный дождь',
        'continuous-heavy-rain': 'длительный сильный дождь',
        'showers': 'ливень',
        'wet-snow': 'дождь со снегом',
        'light-snow': 'небольшой снег',
        'snow': 'снег',
        'snow-showers': 'снегопад',
        'hail': 'град',
        'thunderstorm': 'гроза',
        'thunderstorm-with-rain': 'дождь с грозой',
        'thunderstorm-with-hail': 'гроза с градом'
    }

    forecasts = weather_data['forecasts']
    for forecast in forecasts:
        date = forecast['date']
        day_forecast = forecast['parts']['day']
        night_forecast = forecast['parts']['night']

        print(f"Прогноз на {date} в локации {city_name}:")
        print(f"Днем: {day_forecast['temp_avg']}°C, {weather_dict[day_forecast['condition']]}")
        print(f"Ночью: {night_forecast['temp_avg']}°C, {weather_dict[night_forecast['condition']]}")
        print()


parser = argparse.ArgumentParser(description="Прогноз погоды в указанном городе")
parser.add_argument("--opencage-api-key", type=str, help="API ключ OpenCage Geocoder")
parser.add_argument("--yandex-api-key", type=str, help="API ключ Яндекс.Погода")
args = parser.parse_args()

city_name = input("Введите название города: ")


if args.opencage_api_key:
    api_key = args.opencage_api_key
else:
    print("Не указан API ключ OpenCage API.")
    exit()

coordinates = get_coordinates(api_key, city_name)

if coordinates:
    latitude, longitude = coordinates
    print(f"Широта: {latitude}")
    print(f"Долгота: {longitude}")
else:
    print("Не удалось найти координаты для указанного города.")
    exit()


if args.yandex_api_key:
    weather_data = request_yandex_weather_api(args.yandex_api_key, latitude, longitude)
else:
    print("Не указан API ключ Яндекс.Погода.")
    exit()


date_input = input("Пожалуйста, введите дату (в формате ГГГГ-ММ-ДД): ")

found_forecast = None
for forecast in weather_data['forecasts']:
    if forecast["date"] == date_input:
        found_forecast = forecast
        break

if found_forecast:
    print_weather_forecast({'forecasts': [found_forecast]})
else:
    print("Прогноз погоды для указанной даты не найден.")
