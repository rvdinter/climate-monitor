"""Class for PM sensor."""
import time
import board
from busio import UART
from adafruit_pm25.uart import PM25_UART

class ParticulateMatter():
    """PM sensor."""
    
    def __init__(self, reset_pin=None):
        uart = UART(board.TX, board.RX, baudrate=9600)
        self.pm25 = PM25_UART(uart, reset_pin)
        
    def get_data(self):
        """
        Get data of PM sensor.

        Returns
        -------
        pmdata : string
            data read from PM sensor.

        """
        try:
            pm_data = self.pm25.read()
            return pm_data
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            
if __name__ == "__main__":
    pm = ParticulateMatter()
    print("Found PM2.5 sensor, reading data...")
    
    while True:
        time.sleep(1)
        pm_data = pm.get_data()
        print()
        print("Concentration Units (standard)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (pm_data["pm10 standard"], pm_data["pm25 standard"], pm_data["pm100 standard"])
        )
        print("Concentration Units (environmental)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (pm_data["pm10 env"], pm_data["pm25 env"], pm_data["pm100 env"])
        )
        print("---------------------------------------")
        print("Particles > 0.3um / 0.1L air:", pm_data["particles 03um"])
        print("Particles > 0.5um / 0.1L air:", pm_data["particles 05um"])
        print("Particles > 1.0um / 0.1L air:", pm_data["particles 10um"])
        print("Particles > 2.5um / 0.1L air:", pm_data["particles 25um"])
        print("Particles > 5.0um / 0.1L air:", pm_data["particles 50um"])
        print("Particles > 10 um / 0.1L air:", pm_data["particles 100um"])
        print("---------------------------------------")

        