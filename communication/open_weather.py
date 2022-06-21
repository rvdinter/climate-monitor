import json
import urllib.error
from urllib.parse import urlencode

from urllib.request import urlopen


class OpenWeather:
    def __init__(self, api_key):
        self._api_key = api_key
        self.data_source_url = "http://api.openweathermap.org/data/2.5/weather"

        if len(self._api_key) == 0:
            raise RuntimeError(
                "You need to set your token first. If you don't already have one, you can register for a free account "
                "at https://home.openweathermap.org/users/sign_up"
            )

    def get_weather(self, location):
        params = {"q": location, "appid": self._api_key}
        data_source = self.data_source_url + "?" + urlencode(params)
        value = None
        try:
            response = urlopen(data_source)
            if response.getcode() == 200:
                value = response.read()
        except urllib.error.HTTPError:
            print("Could not get the HTTP response")
        weather = json.loads(value.decode("utf-8"))
        return weather


if __name__ == '__main__':
    api_key = json.load(open('../config.json'))['openweather']['api_key']
    ow = OpenWeather(api_key)
    weather = ow.get_weather('Arnhem, NL')
    print(weather)
