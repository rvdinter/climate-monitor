"""Class for PM sensor."""
import time

import board
from adafruit_pm25.uart import PM25_UART
from busio import UART

from sensor_base import SensorBase


class ParticulateMatter(SensorBase):
    """PM sensor."""

    def __init__(self):
        super().__init__(__name__)
        uart = UART(board.TX, board.RX, baudrate=9600)
        self._pm25 = PM25_UART(uart, reset_pin=None)
        self._read_attempts = 0

    def get_data(self):
        """
        Get data of PM sensor.

        Returns
        -------
        pm_data : dict
            data read from PM sensor.

        """
        try:
            pm_data = self._pm25.read()
            self._read_attempts = 0
            return pm_data
        except RuntimeError:
            if self._read_attempts < 30:
                print("Unable to read from sensor, retrying...")
            else:
                raise RuntimeError(f"Unable to read sensor after {self._read_attempts} attempts.")

    @staticmethod
    def show_data(pm_data):
        """

        :param pm_data:
        """
        print("\nConcentration Units (standard)")
        print("---------------------------------------")
        print(f"PM 1.0: {pm_data['pm10 standard']}\t"
              f"PM2.5: {pm_data['pm25 standard']}\t"
              f"PM10: {pm_data['pm100 standard']}")
        print("Concentration Units (environmental)")
        print("---------------------------------------")
        print(f"PM 1.0: {pm_data['pm10 env']}\t"
              f"PM2.5: {pm_data['pm25 env']}\t"
              f"PM10: {pm_data['pm100 env']}")
        print("---------------------------------------")
        print(f"Particles > 0.3um / 0.1L air: {pm_data['particles 03um']}")
        print(f"Particles > 0.5um / 0.1L air: {pm_data['particles 05um']}")
        print(f"Particles > 1.0um / 0.1L air: {pm_data['particles 10um']}")
        print(f"Particles > 2.5um / 0.1L air: {pm_data['particles 25um']}")
        print(f"Particles > 5.0um / 0.1L air: {pm_data['particles 50um']}")
        print(f"Particles > 10 um / 0.1L air: {pm_data['particles 100um']}")
        print("---------------------------------------")


if __name__ == "__main__":
    pm = ParticulateMatter()
    print("Found PM2.5 sensor, reading data...")

    while True:
        time.sleep(1)
        pm_data = pm.get_data()
        pm.show_data(pm_data)
