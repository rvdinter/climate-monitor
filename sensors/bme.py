"""Class for BME680 sensor."""
import time
import board
from adafruit_bme680 import Adafruit_BME680_I2C

from sensor_base import SensorBase


class BME680(SensorBase):
    """BME680 class."""

    def __init__(self, temperature_offset: float, humidity_baseline: float = 40.0):
        # Create library object using our Bus I2C port
        super().__init__(__name__)
        i2c = board.I2C()
        self._bme680 = Adafruit_BME680_I2C(i2c)
        # change this to match the location's pressure (hPa) at sea level
        self._bme680.sea_level_pressure = 1013.25

        self._temperature_offset = temperature_offset
        self._humidity_baseline = humidity_baseline
        print("BME found. Generating gas baseline...")
        self._gas_baseline = self._get_gas_baseline()
        print("Done with generating gas baseline.")

    def get_data(self):
        """
        Get all data from the BME680.

        Returns
        -------
        dict
            all information from the sensor.
        """
        return {'temp': self._bme680.temperature - self._temperature_offset,
                'gas': self._bme680.gas,
                'humidity': self._bme680.relative_humidity,
                'pressure': self._bme680.pressure,
                'altitude': self._bme680.altitude}

    def _get_gas_baseline(self):
        """
        Get the gas baseline.

        Returns
        -------
        None.

        """
        start_time = time.time()
        curr_time = time.time()
        burn_in_time = 300

        burn_in_data = []

        # Collect gas resistance burn-in values, then use the average
        # of the last 50 values to set the upper limit for calculating
        # gas_baseline.
        print('Collecting gas resistance burn-in data for 5 mins\n')
        while curr_time - start_time < burn_in_time:
            curr_time = time.time()
            gas = self._bme680.gas
            burn_in_data.append(gas)
            print('Gas: {0} Ohms'.format(gas))
            time.sleep(1)

        return sum(burn_in_data[-50:]) / 50.0

    def calculate_iaq(self, hum_weighting=0.25):
        """
        Calculate Indoor Air Quality.

        Parameters
        ----------
        hum_weighting : float, optional
            weighting for humidity vs gas. The default is 0.25.

        Returns
        -------
        iaq : float
            a quality score between 0 and 1600.
        """
        print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(self._gas_baseline,
                                                                                self._humidity_baseline))

        gas_offset = self._gas_baseline - self._bme680.gas
        hum_offset = self._bme680.relative_humidity - self._humidity_baseline

        # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - self._humidity_baseline - hum_offset)
            hum_score /= (100 - self._humidity_baseline)
            hum_score *= (hum_weighting * 100)

        else:
            hum_score = (self._humidity_baseline + hum_offset)
            hum_score /= self._humidity_baseline
            hum_score *= (hum_weighting * 100)

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (self._bme680.gas / self._gas_baseline)
            gas_score *= (100 - (hum_weighting * 100))

        else:
            gas_score = 100 - (hum_weighting * 100)

        # Calculate iaq.
        iaq = hum_score + gas_score
        return iaq


if __name__ == "__main__":
    temp_offset = 5
    bme = BME680(temperature_offset=5)

    print(f"One data sample: {bme.get_data()}")

    print("Calculating IAQ for 30 seconds...")
    for i in range(30):
        time.sleep(1)
        iaq = bme.calculate_iaq()
        print(f"{i}: IAQ: {iaq}")
