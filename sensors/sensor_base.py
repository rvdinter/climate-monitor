class SensorBase:
    def __init__(self, name: str):
        self.name = name
        print(f"Sensor {self.name} initialized!")

    def get_data(self):
        raise NotImplementedError(f"Get data for {self.name} not implemented!")
