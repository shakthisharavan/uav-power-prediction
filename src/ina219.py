"""
INA219 Sensor Module for Reading Voltage, Current, and Power
"""

import smbus2
import time
import logging
from typing import Tuple, Optional

class INA219:
    """
    Driver for Texas Instruments INA219 current/power monitor
    Communicates over I2C bus
    """

    # INA219 Registers
    REG_CONFIG = 0x00
    REG_SHUNT_VOLTAGE = 0x01
    REG_BUS_VOLTAGE = 0x02
    REG_POWER = 0x03
    REG_CURRENT = 0x04
    REG_CALIBRATION = 0x05

    def __init__(self, i2c_bus: int = 1, i2c_address: int = 0x40):
        """
        Initialize INA219 sensor

        Args:
            i2c_bus: I2C bus number (default: 1 for Raspberry Pi)
            i2c_address: I2C address of INA219 (default: 0x40)
        """
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address
        self.bus = smbus2.SMBus(self.i2c_bus)
        self.logger = logging.getLogger(__name__)

        # Calibration values (will be set during configuration)
        self._cal_value = 0
        self._power_lsb = 0
        self._current_lsb = 0

        # Try to initialize the sensor
        try:
            self._configure()
            self.logger.info(f"INA219 initialized on bus {i2c_bus}, address 0x{i2c_address:02x}")
        except Exception as e:
            self.logger.error(f"Failed to initialize INA219: {e}")
            raise

    def _configure(self):
        """Configure the INA219 for operation"""
        # Reset the device
        self.bus.write_word_data(self.i2c_address, self.REG_CONFIG, 0x8000)
        time.sleep(0.01)  # Wait for reset

        # Set calibration for 32V, 2A range
        # These values are for typical configuration
        # In practice, these should be calculated based on shunt resistor value
        self._cal_value = 0x0400  # Example calibration value
        self._power_lsb = 0.01    # 10mW per bit
        self._current_lsb = 0.001 # 1mA per bit

        # Write calibration register
        self.bus.write_word_data(self.i2c_address, self.REG_CALIBRATION, self._cal_value)

        # Configure register: enable continuous shunt and bus voltage measurement
        config = 0x019F  # Default configuration: 32V range, PGA=8, 12-bit bus, 12-bit shunt
        self.bus.write_word_data(self.i2c_address, self.REG_CONFIG, config)

    def read_shunt_voltage(self) -> float:
        """
        Read shunt voltage in volts

        Returns:
            Shunt voltage in volts
        """
        try:
            raw = self.bus.read_word_data(self.i2c_address, self.REG_SHUNT_VOLTAGE)
            # Swap bytes (INA219 returns data in big-endian but we read as little-endian)
            raw = ((raw << 8) & 0xFF00) | (raw >> 8)
            # Convert to signed 16-bit value
            if raw > 0x7FFF:
                raw -= 0x10000
            # LSB = 10µV (for typical configuration)
            voltage = raw * 0.00001
            return voltage
        except Exception as e:
            self.logger.error(f"Error reading shunt voltage: {e}")
            return 0.0

    def read_bus_voltage(self) -> float:
        """
        Read bus voltage in volts

        Returns:
            Bus voltage in volts
        """
        try:
            raw = self.bus.read_word_data(self.i2c_address, self.REG_BUS_VOLTAGE)
            # Swap bytes
            raw = ((raw << 8) & 0xFF00) | (raw >> 8)
            # Right shift 3 bits (CNVR/BUSY/OVF bits are top 3 bits)
            raw >>= 3
            # LSB = 4mV
            voltage = raw * 0.004
            return voltage
        except Exception as e:
            self.logger.error(f"Error reading bus voltage: {e}")
            return 0.0

    def read_current(self) -> float:
        """
        Read current in amperes

        Returns:
            Current in amperes
        """
        try:
            raw = self.bus.read_word_data(self.i2c_address, self.REG_CURRENT)
            # Swap bytes
            raw = ((raw << 8) & 0xFF00) | (raw >> 8)
            # Convert to signed 16-bit value
            if raw > 0x7FFF:
                raw -= 0x10000
            current = raw * self._current_lsb
            return current
        except Exception as e:
            self.logger.error(f"Error reading current: {e}")
            return 0.0

    def read_power(self) -> float:
        """
        Read power in watts

        Returns:
            Power in watts
        """
        try:
            raw = self.bus.read_word_data(self.i2c_address, self.REG_POWER)
            # Swap bytes
            raw = ((raw << 8) & 0xFF00) | (raw >> 8)
            power = raw * self._power_lsb
            return power
        except Exception as e:
            self.logger.error(f"Error reading power: {e}")
            return 0.0

    def read_all(self) -> Tuple[float, float, float, float]:
        """
        Read all measurements: shunt voltage, bus voltage, current, power

        Returns:
            Tuple of (shunt_voltage, bus_voltage, current, power)
        """
        shunt_v = self.read_shunt_voltage()
        bus_v = self.read_bus_voltage()
        current = self.read_current()
        power = self.read_power()
        return shunt_v, bus_v, current, power

    def close(self):
        """Close the I2C bus connection"""
        try:
            self.bus.close()
        except Exception as e:
            self.logger.error(f"Error closing I2C bus: {e}")

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sensor = INA219()

    try:
        while True:
            shunt_v, bus_v, current, power = sensor.read_all()
            print(f"Shunt Voltage: {shunt_v:.3f} V")
            print(f"Bus Voltage: {bus_v:.3f} V")
            print(f"Current: {current:.3f} A")
            print(f"Power: {power:.3f} W")
            print("-" * 30)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sensor.close()