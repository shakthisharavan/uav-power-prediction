"""
Sensor Fusion Module for Combining Readings from Multiple Sensors
"""

import logging
from typing import Dict, Optional, Tuple
from .ina219 import INA219
from .ds18b20 import DS18B20

class SensorHub:
    """
    Hub for managing multiple sensors and providing unified readings
    """

    def __init__(self,
                 ina219_bus: int = 1,
                 ina219_address: int = 0x40,
                 ds18b20_id: Optional[str] = None):
        """
        Initialize sensor hub

        Args:
            ina219_bus: I2C bus for INA219
            ina219_address: I2C address for INA219
            ds18b20_id: Specific DS18B20 sensor ID (optional)
        """
        self.logger = logging.getLogger(__name__)

        # Initialize sensors
        try:
            self.ina219 = INA219(i2c_bus=ina219_bus, i2c_address=ina219_address)
            self.logger.info("INA219 sensor initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize INA219: {e}")
            self.ina219 = None

        try:
            self.ds18b20 = DS18B20(sensor_id=ds18b20_id)
            self.logger.info("DS18B20 sensor initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize DS18B20: {e}")
            self.ds18b20 = None

        # Track initialization status
        self.sensors_initialized = {
            'ina219': self.ina219 is not None,
            'ds18b20': self.ds18b20 is not None
        }

    def read_ina219(self) -> Dict[str, float]:
        """
        Read all INA219 measurements

        Returns:
            Dictionary with voltage, current, power readings
        """
        if not self.ina219:
            return {'voltage': 0.0, 'current': 0.0, 'power': 0.0, 'shunt_voltage': 0.0}

        try:
            shunt_v, bus_v, current, power = self.ina219.read_all()
            # For this application, we're primarily interested in bus voltage
            # which represents the system voltage being monitored
            return {
                'shunt_voltage': shunt_v,
                'voltage': bus_v,  # Bus voltage is the main voltage measurement
                'current': current,
                'power': power
            }
        except Exception as e:
            self.logger.error(f"Error reading INA219: {e}")
            return {'voltage': 0.0, 'current': 0.0, 'power': 0.0, 'shunt_voltage': 0.0}

    def read_ds18b20(self) -> float:
        """
        Read temperature from DS18B20

        Returns:
            Temperature in Celsius
        """
        if not self.ds18b20:
            return 0.0

        try:
            return self.ds18b20.read_temperature()
        except Exception as e:
            self.logger.error(f"Error reading DS18B20: {e}")
            return 0.0

    def read_all(self) -> Dict[str, float]:
        """
        Read all sensor measurements

        Returns:
            Dictionary containing all sensor readings
        """
        readings = {}

        # Read INA219 data
        ina219_data = self.read_ina219()
        readings.update({
            'voltage': ina219_data['voltage'],
            'current': ina219_data['current'],
            'power': ina219_data['power'],
            'shunt_voltage': ina219_data['shunt_voltage']
        })

        # Read DS18B20 data
        temperature = self.read_ds18b20()
        readings['temperature'] = temperature

        return readings

    def get_sensor_status(self) -> Dict[str, bool]:
        """
        Get initialization status of all sensors

        Returns:
            Dictionary indicating which sensors are initialized
        """
        return self.sensors_initialized.copy()

    def close(self):
        """Close all sensor connections"""
        if self.ina219:
            try:
                self.ina219.close()
            except Exception as e:
                self.logger.error(f"Error closing INA219: {e}")

        # DS18B20 doesn't need explicit closing in this implementation

# Convenience function for quick sensor reading
def read_all_sensors() -> Dict[str, float]:
    """
    Quick function to read all sensors (creates and destroys SensorHub)

    Returns:
        Dictionary containing all sensor readings
    """
    hub = SensorHub()
    try:
        return hub.read_all()
    finally:
        hub.close()

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    hub = SensorHub()

    try:
        print("Sensor Hub Status:", hub.get_sensor_status())
        print("-" * 40)

        while True:
            readings = hub.read_all()
            print(f"Voltage: {readings['voltage']:.3f} V")
            print(f"Current: {readings['current']:.3f} A")
            print(f"Power: {readings['power']:.3f} W")
            print(f"Temperature: {readings['temperature']:.2f}°C")
            print(f"Shunt Voltage: {readings['shunt_voltage']:.6f} V")
            print("-" * 40)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        hub.close()