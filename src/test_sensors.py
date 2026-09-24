"""
Test Script for Verifying Sensor Module Functionality
"""

import sys
import time
import logging
from .ina219 import INA219
from .ds18b20 import DS18B20
from .oled import OLEDDisplay
from .sensors import SensorHub
from .data_logger import DataLogger

def test_ina219():
    """Test INA219 sensor functionality"""
    print("Testing INA219 sensor...")
    try:
        sensor = INA219()
        shunt_v, bus_v, current, power = sensor.read_all()
        print(f"  Shunt Voltage: {shunt_v:.6f} V")
        print(f"  Bus Voltage: {bus_v:.3f} V")
        print(f"  Current: {current:.3f} A")
        print(f"  Power: {power:.3f} W")
        sensor.close()
        print("  ✓ INA219 test passed")
        return True
    except Exception as e:
        print(f"  ✗ INA219 test failed: {e}")
        return False

def test_ds18b20():
    """Test DS18B20 sensor functionality"""
    print("Testing DS18B20 sensor...")
    try:
        sensor = DS18B20()
        temp_c = sensor.read_temperature()
        temp_f = sensor.read_temperature_fahrenheit()
        print(f"  Temperature: {temp_c:.2f}°C / {temp_f:.2f}°F")
        print("  ✓ DS18B20 test passed")
        return True
    except Exception as e:
        print(f"  ✗ DS18B20 test failed: {e}")
        return False

def test_oled():
    """Test OLED display functionality"""
    print("Testing OLED display...")
    try:
        display = OLEDDisplay()
        display.display_text(["Test", "OLED", "Display"])
        time.sleep(1)
        display.display_sensor_data(12.5, 0.842, 10.53, 31.5)
        time.sleep(1)
        display.clear()
        print("  ✓ OLED test passed")
        return True
    except Exception as e:
        print(f"  ✗ OLED test failed: {e}")
        return False

def test_sensors():
    """Test sensor fusion functionality"""
    print("Testing Sensor Hub...")
    try:
        hub = SensorHub()
        status = hub.get_sensor_status()
        print(f"  Sensor Status: {status}")

        readings = hub.read_all()
        print(f"  Voltage: {readings['voltage']:.3f} V")
        print(f"  Current: {readings['current']:.3f} A")
        print(f"  Power: {readings['power']:.3f} W")
        print(f"  Temperature: {readings['temperature']:.2f}°C")

        hub.close()
        print("  ✓ Sensor Hub test passed")
        return True
    except Exception as e:
        print(f"  ✗ Sensor Hub test failed: {e}")
        return False

def test_data_logger():
    """Test data logger functionality"""
    print("Testing Data Logger...")
    try:
        logger = DataLogger(data_dir="/tmp/test_pbl_data")
        logger.start_experiment("test_experiment")

        # Log some test data
        test_readings = [
            {'voltage': 12.1, 'current': 0.5, 'power': 6.05, 'temperature': 25.0},
            {'voltage': 12.2, 'current': 0.52, 'power': 6.34, 'temperature': 25.1},
            {'voltage': 12.0, 'current': 0.48, 'power': 5.76, 'temperature': 24.9}
        ]

        for readings in test_readings:
            logger.log_reading(readings)

        logger.stop_experiment()
        size = logger.get_log_file_size()
        print(f"  Log file size: {size} bytes")

        if size > 0:
            print("  ✓ Data Logger test passed")
            return True
        else:
            print("  ✗ Data Logger test failed: No data written")
            return False
    except Exception as e:
        print(f"  ✗ Data Logger test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("PBL Sensor Module Test Suite")
    print("=" * 50)

    tests = [
        test_ina219,
        test_ds18b20,
        test_oled,
        test_sensors,
        test_data_logger
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)  # Reduce verbosity for testing
    sys.exit(main())