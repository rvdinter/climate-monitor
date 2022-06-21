# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

small_font = ImageFont.truetype(
    # "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    r"C:\Windows\Fonts\arial.ttf",
    12
)
medium_font = ImageFont.truetype(
    # "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    r"C:\Windows\Fonts\arial.ttf",
    20
)
large_font = ImageFont.truetype(
    # "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    24
)
icon_font = ImageFont.truetype("./meteocons.ttf", 48)

# Map the OpenWeatherMap icon code to the appropriate font character
# See http://www.alessioatzeni.com/meteocons/ for icons
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Graphics:
    def __init__(self, display, *, am_pm=True, celsius=True):
        self.am_pm = am_pm
        self.celsius = celsius

        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self.display = display
        self.display_width = 250
        self.display_height = 122

        self._weather_icon = None
        self._city_name = None
        self._main_text = None
        self._temperature = None
        self._description = None
        self._time_text = None

    def set_weather(self, weather):

        # set the icon/background
        self._weather_icon = ICON_MAP[weather["weather"][0]["icon"]]

        city_name = weather["name"] + ", " + weather["sys"]["country"]
        self._city_name = city_name

        main = weather["weather"][0]["main"]
        self._main_text = main

        temperature = weather["main"]["temp"] - 273.15  # convert kelvin to celsius
        if self.celsius:
            self._temperature = "%d °C" % temperature
        else:
            self._temperature = "%d °F" % ((temperature * 9 / 5) + 32)

        description = weather["weather"][0]["description"]
        description = description[0].upper() + description[1:]
        self._description = description

    def set_pm_data(self, pm_data):
        self.pm_data = pm_data

    def set_bme_data(self, bme_data):
        self.bme_data = bme_data

    def set_aqi_data(self, aqi_data):
        self.aqi_data = aqi_data

    def get_time(self):
        now = datetime.now()
        if self.am_pm:
            time_format = "%I:%M %p"
        else:
            time_format = "%H:%M"

        self._time_text = now.strftime(time_format).lstrip("0").replace(" 0", " ")

    def update_display(self):
        # self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display_width, self.display_height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the Icon
        (font_width, font_height) = icon_font.getsize(self._weather_icon)
        draw.text(
            (
                self.display_width - font_width - 5,
                0,
            ),
            self._weather_icon,
            font=icon_font,
            fill=BLACK,
        )

        # Draw the outdoor temperature
        (font_width, font_height) = large_font.getsize(self._temperature)
        draw.text(
            (
                (self.display_width - font_width ) - font_width,
                15,
            ),
            self._temperature,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw the city
        draw.text(
            (5, 5), self._city_name, font=self.small_font, fill=BLACK,
        )

        # Draw the time
        (font_width, font_height) = medium_font.getsize(self._time_text)
        draw.text(
            (5, font_height ),
            self._time_text,
            font=self.medium_font,
            fill=BLACK,
        )

        # # Draw the main text
        # (font_width, font_height) = large_font.getsize(self._main_text)
        # draw.text(
        #     (5, self.display_height - font_height * 2),
        #     self._main_text,
        #     font=self.large_font,
        #     fill=BLACK,
        # )

        # # Draw the description
        # (font_width, font_height) = small_font.getsize(self._description)
        # draw.text(
        #     (5, self.display_height - font_height - 5),
        #     self._description,
        #     font=self.small_font,
        #     fill=BLACK,
        # )

        # Draw the indoor temperature
        indoor_temp = f"{self.bme_data['temp']:.0f} °C"
        (font_width, font_height) = large_font.getsize(indoor_temp)
        draw.text(
            (
                self.display_width - font_width - 5,
                self.display_height - font_height * 2,
            ),
            indoor_temp,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw the AQI
        aqi = f"AQI: {aqi_data:.0f}"
        (font_width, font_height) = icon_font.getsize(aqi)
        draw.text(
            (
                5,
                self.display_height // 2 - font_height // 2,
            ),
            aqi,
            font=large_font,
            fill=BLACK,
        )

        # Draw the PM
        draw.rectangle((0, self.display_height - 15, self.display_width, self.display_height), fill=BLACK)
        pm_text = (f"PM 1.0: {pm_data['pm10 standard']}    "
              f"PM2.5: {pm_data['pm25 standard']}    "
              f"PM10: {pm_data['pm100 standard']}")
        (font_width, font_height) = small_font.getsize(pm_text)
        draw.text(
            (5, self.display_height - font_height - 3),
            pm_text,
            font=self.small_font,
            fill=WHITE,
        )
        return image
        # self.display.image(image)
        # self.display.display()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    weather = {'coord': {'lon': 5.9, 'lat': 51.9667},
               'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}],
               'base': 'stations',
               'main': {'temp': 292.55, 'feels_like': 292.09, 'temp_min': 291.43, 'temp_max': 293.69, 'pressure': 1013,
                        'humidity': 59},
               'visibility': 10000,
               'wind': {'speed': 2.24, 'deg': 340, 'gust': 0},
               'clouds': {'all': 100},
               'dt': 1655839632,
               'sys': {'type': 2, 'id': 2037908, 'country': 'NL', 'sunrise': 1655781381, 'sunset': 1655841594},
               'timezone': 7200, 'id': 2759660, 'name': 'Gemeente Arnhem', 'cod': 200}

    bme_data = {'temp': 20.15354,
                'gas': 6846843,
                'humidity': 40.325,
                'pressure': 1068.35684,
                'altitude': 10.358}
    pm_data = {'pm10 standard': 15, 'pm25 standard': 20, 'pm100 standard': 800}
    aqi_data = 20.32

    gfx = Graphics(None, am_pm=False, celsius=True)
    gfx.set_pm_data(pm_data)
    gfx.set_bme_data(bme_data)
    gfx.set_aqi_data(aqi_data)
    gfx.set_weather(weather)
    gfx.get_time()
    img = gfx.update_display()
    plt.imshow(img)
    plt.show()
