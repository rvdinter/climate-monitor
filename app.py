import time
import json

from ui.graphics import Graphics
from sensors.bme import BME680
from sensors.particulate_matter import ParticulateMatter
from communication.open_weather import OpenWeather
import matplotlib.pyplot as plt

api_key = json.load(open('../config.json'))['openweather']['api_key']
temp_offset = 5

if __name__ == '__main__':
    gfx = Graphics(None, am_pm=False, celsius=True)
    ow = OpenWeather(api_key)
    # bme = BME680(temperature_offset=temp_offset)
    # pm = ParticulateMatter()

    while True:
        time.sleep(60)
        weather = ow.get_weather('Arnhem, NL')
        bme_data = {'temp': 20.15354,
                'gas': 6846843,
                'humidity': 40.325,
                'pressure': 1068.35684,
                'altitude': 10.358}
        pm_data = {'pm10 standard': 15, 'pm25 standard': 20, 'pm100 standard': 800}
        aqi_data = 20.32

        gfx.set_weather(weather)
        gfx.get_time()
        img = gfx.update_display()
        plt.imshow(img)
        plt.show()