"""Platform for sensor integration."""
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE
from homeassistant.helpers.entity import Entity
import psutil
import board
#from ina219 import INA219
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ExampleSensor()])


class ExampleSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        i2c_bus = board.I2C()
        self.ina219 = INA219(i2c_bus)
        self._state = round(self.ina219.current, 2)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'INA219 Example'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "mA"

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = round(self.ina219.current, 2)
