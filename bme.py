"""Class for BME680 sensor."""
import time
import board
from digitalio import I2C
from  adafruit_bme680 import Adafruit_BME680_I2C

class BME():
    """BME680 class."""
    
    def __init__(self, humidity_baseline=40.0):
        # Create library object using our Bus I2C port
        i2c = I2C(board.SCL, board.SDA)
        self.bme680 = Adafruit_BME680_I2C(i2c)
        # change this to match the location's pressure (hPa) at sea level
        self.bme680.sea_level_pressure = 1013.25
        self.humidity_baseline = humidity_baseline
        print("BME found. Generating gas baseline...")
        self.get_gas_baseline()
        print("Done with generating gas baseline.")
        
    def get_data(self, temp_offset):
        """
        Get all data from the BME680.

        Parameters
        ----------
        temp_offset : float
            offset to make the temperature meter more precise.

        Returns
        -------
        dict
            all information from the sensor.

        """
        return {'temp': self.bme680.temperature-temp_offset, 
                'gas': self.bme680.gas, 
                'humidity': self.bme680.relative_humidity, 
                'pressure': self.bme680.pressure, 
                'altitude': self.bme680.altitude}

    def get_gas_baseline(self):
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
            gas = self.bme680.gas
            burn_in_data.append(gas)
            print('Gas: {0} Ohms'.format(gas))
            time.sleep(1)
    
        self.gas_baseline = sum(burn_in_data[-50:]) / 50.0
    
    def calculate_iaq(self, hum_weighting = 0.25):
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
        iaq_warn : bool
            warn if the iaq is of low quality.

        """
        iaq_warn = False
        print('Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n'.format(self.gas_baseline, self.humidity_baseline))
    
        gas_offset = self.gas_baseline - self.bme680.gas
        hum_offset = self.bme680.hum - self.hum_baseline
    
        # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - self.hum_baseline - hum_offset)
            hum_score /= (100 - self.hum_baseline)
            hum_score *= (hum_weighting * 100)
    
        else:
            hum_score = (self.hum_baseline + hum_offset)
            hum_score /= self.hum_baseline
            hum_score *= (hum_weighting * 100)
    
        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (self.bme680.gas / self.gas_baseline)
            gas_score *= (100 - (hum_weighting * 100))
    
        else:
            gas_score = 100 - (hum_weighting * 100)
    
        # Calculate iaq.
        iaq = hum_score + gas_score
        return iaq, iaq_warn
    
if __name__ == "__main__":
    bme = BME()
    
    temp_offset = 5
    print("One data sample: " + bme.get_data(temp_offset))
    
    print("Calculating IAQ...")
    while True:
        time.sleep(1)
        iaq, iaq_warn = bme.calculate_iaq()
        print("IAQ: " + iaq)