"""
DS18B20 Temperature Sensor Module
"""

import os
import glob
import time
import logging
from typing import Optional

class DS18B20:
    """
    Driver for Maxim DS18B20 digital temperature sensor
    Communicates over 1-Wire interface
    """

    def __init__(self, sensor_id: Optional[str] = None):
        """
        Initialize DS18B20 sensor

        Args:
            sensor_id: Specific sensor ID to use (if None, uses first found)
        """
        self.logger = logging.getLogger(__name__)
        self.base_dir = '/sys/bus/w1/devices/'

        # Find device folder
        self.device_folder = self._find_device(sensor_id)
        if self.device_folder is None:
            raise RuntimeError("DS18B20 sensor not found")

        self.device_file = os.path.join(self.device_folder, 'w1_slave')
        self.logger.info(f"DS18B20 initialized: {self.device_folder}")

    def _find_device(self, sensor_id: Optional[str] = None) -> Optional[str]:
        """
        Find DS18B20 device folder

        Args:
            sensor_id: Specific sensor ID to look for

        Returns:
            Path to device folder or None if not found
        """
        # Load 1-Wire kernel modules if not already loaded
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        # Find device folders
        device_folders = glob.glob(self.base_dir + '28*')

        if not device_folders:
            self.logger.error("No DS18B20 sensors found")
            return None

        if sensor_id is None:
            # Use first sensor found
            return device_folders[0]
        else:
            # Look for specific sensor ID
            for folder in device_folders:
                if sensor_id in folder:
                    return folder
            self.logger.error(f"DS18B20 sensor with ID {sensor_id} not found")
            return None

    def _read_temp_raw(self) -> list:
        """
        Read raw temperature data from sensor

        Returns:
            List of lines from sensor file
        """
        try:
            with open(self.device_file, 'r') as f:
                lines = f.readlines()
            return lines
        except Exception as e:
            self.logger.error(f"Error reading from DS18B20: {e}")
            return []

    def read_temperature(self) -> float:
        """
        Read temperature in Celsius

        Returns:
            Temperature in degrees Celsius
        """
        lines = self._read_temp_raw()
        if not lines:
            return 0.0

        # Wait for valid reading
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
            if not lines:
                return 0.0

        # Extract temperature value
        equals_pos = lines[1].find('t=')
        if equals_pos == -1:
            self.logger.error("Temperature value not found in sensor data")
            return 0.0

        temp_string = lines[1][equals_pos+2:]
        try:
            temp_c = float(temp_string) / 1000.0
            return temp_c
        except ValueError as e:
            self.logger.error(f"Error converting temperature value: {e}")
            return 0.0

    def read_temperature_fahrenheit(self) -> float:
        """
        Read temperature in Fahrenheit

        Returns:
            Temperature in degrees Fahrenheit
        """
        temp_c = self.read_temperature()
        return temp_c * 9.0 / 5.0 + 32.0

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sensor = DS18B20()

    try:
        while True:
            temp_c = sensor.read_temperature()
            temp_f = sensor.read_temperature_fahrenheit()
            print(f"Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
            print("-" * 30)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")