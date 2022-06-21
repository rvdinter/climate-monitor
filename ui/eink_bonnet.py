import board
import busio
import digitalio
from adafruit_epd.ssd1680 import Adafruit_SSD1680


class EInkBonnet:
    def __init__(self):
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        ecs = digitalio.DigitalInOut(board.CE0)
        dc = digitalio.DigitalInOut(board.D22)
        rst = digitalio.DigitalInOut(board.D27)
        busy = digitalio.DigitalInOut(board.D17)
        self.display = Adafruit_SSD1680(  # Newer eInk Bonnet
            # display = Adafruit_SSD1675(   # Older eInk Bonnet
            width=122, height=250, spi=spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
        )
        self.display.rotation = 1
