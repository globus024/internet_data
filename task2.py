# Azamat Khankhodjaev
# 29.06.2021
# Зарегистрироваться на https://openweathermap.org/api и написать
# функцию, которая получает погоду в данный момент для города, название которого получается через input.

import env
import requests
from typing import Dict



class OpenWheather:
    parametrs = {
        "appid": env.TOKKEN,
        "units": "metric",
        "q": "Tashkent"
    }

    def __init__(self, url: str, city_name: str):
        self.url = url
        self.parametrs['q'] = city_name
        self.wheather ={}

    def _get_response(self, url, params):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        raise ValueError("URL DIE")

    def _parse(self, response: Dict) -> Dict:
        try:
            res = {}
            main = response['main']
            res.update({'temp': main['temp'], 'feels_like':main['feels_like']})
            return res
        except KeyError:
            return []

    def run(self):
        response = self._get_response(self.url, self.parametrs)
        self.wheather = self._parse(response)

    def get_temperature(self):
        try:
            return self.wheather['temp']
        except KeyError:
            return []

if __name__ == '__main__':
    url = "https://api.openweathermap.org/data/2.5/weather"

    city = input(f'Введите название города на английском\n')
    wheather_parse = OpenWheather(url, city_name=city)
    wheather_parse.run()
    print(f'Температура в городе {city} - {wheather_parse.get_temperature()}')
