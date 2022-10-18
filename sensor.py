"""Platform for sensor integration."""
from homeassistant.const import POWER_WATT, ELECTRIC_POTENTIAL_VOLT, ELECTRIC_CURRENT_MILLIAMPERE
from homeassistant.helpers.entity import Entity
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from adafruit_extended_bus import ExtendedI2C as I2C

DEFAULT_ICON = "mdi:current-dc"

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    address = config.get('address')
    device = config.get('device_id')
    device_id = device if device else 1

    add_entities([
        InaCurrent('current', ELECTRIC_CURRENT_MILLIAMPERE, device_id, address), 
        InaCurrent('bus_voltage', ELECTRIC_POTENTIAL_VOLT, device_id, address),
        InaCurrent('shunt_voltage', ELECTRIC_POTENTIAL_VOLT, device_id, address),
        InaCurrent('power', POWER_WATT, device_id, address),
        InaSupply('supply_voltage', ELECTRIC_POTENTIAL_VOLT, device_id, address)
    ])

class InaCurrent(Entity):
    """Representation of a Sensor."""

    def __init__(self, measure, unit, device, address):
        """Initialize the sensor."""
        self._measure = measure
        self._unit = unit
        i2c_bus = I2C(device)
        self._device = device
        self._address = address
        self.ina219 = INA219(i2c_bus, address)
        value = getattr(self.ina219, self._measure)
        self._state = round(value, 2)
        
        if measure == 'bus_voltage':
            InaData.setLastBusVoltage(round(value,2))
        elif measure == 'shunt_voltage':
            InaData.setLastShuntVoltage(round(value,2))
            
    @property
    def unique_id(self):
        """Return the unique ID for this sensor."""
        return 'ina219_dev' + str(self._device) + '_' + hex(self._address) + '_' + self._measure

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._measure.replace('_', ' ').title() + ' ( Dev ' + str(self._device) + ' / INA ' + hex(self._address) + ')'

    @property
    def icon(self):
        """Return the default icon."""
        return DEFAULT_ICON

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    def update(self):
        """Fetch new state data for the sensor."""
        value = getattr(self.ina219, self._measure)
        self._state = round(value, 2)
        
        if self._measure == 'bus_voltage':
            InaData.setLastBusVoltage(round(value,2))
        elif self._measure == 'shunt_voltage':
            InaData.setLastShuntVoltage(round(value,2))

class InaSupply(Entity):
    """Representation of a Sensor."""

    def __init__(self, measure, unit, device, address):
        """Initialize the sensor."""
        self._measure = measure
        self._unit = unit
        self._device = device
        self._address = address
        self._state = InaData.getLastBusVoltage() + InaData.getLastShuntVoltage()
            
    @property
    def unique_id(self):
        """Return the unique ID for this sensor."""
        return 'ina219_dev' + str(self._device) + '_' + hex(self._address) + '_' + self._measure

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._measure.replace('_', ' ').title() + ' ( Dev ' + str(self._device) + ' / INA ' + hex(self._address) + ')'

    @property
    def icon(self):
        """Return the default icon."""
        return DEFAULT_ICON

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    def update(self):
        """Fetch new state data for the sensor."""
        self._state = InaData.getLastBusVoltage() + InaData.getLastShuntVoltage()


class InaData:

    def setLastBusVoltage(currentBusVoltage):
        InaData.lastBusVoltage = currentBusVoltage
    
    def setLastShuntVoltage(currentShuntVoltage):
        InaData.lastShuntVoltage = currentShuntVoltage
        
    def getLastBusVoltage():
        return InaData.lastBusVoltage
    
    def getLastShuntVoltage():
        return InaData.lastShuntVoltage
