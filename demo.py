"""
Demo Script for PBL Sensor Modules
This script demonstrates how to use the sensor modules without requiring actual hardware.
It uses mock/simulated data to show the API usage.
"""

import sys
import os

# Add src directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_ina219():
    """Demonstrate INA219 module usage"""
    print("=" * 50)
    print("INA219 Module Demo")
    print("=" * 50)
    print("Usage example:")
    print("  from src.ina219 import INA219")
    print("  sensor = INA219(i2c_bus=1, i2c_address=0x40)")
    print("  shunt_v, bus_v, current, power = sensor.read_all()")
    print("  sensor.close()")
    print()
    print("Note: Actual hardware required for real readings")
    print()

def demo_ds18b20():
    """Demonstrate DS18B20 module usage"""
    print("=" * 50)
    print("DS18B20 Module Demo")
    print("=" * 50)
    print("Usage example:")
    print("  from src.ds18b20 import DS18B20")
    print("  sensor = DS18B20()  # Auto-detects first sensor")
    print("  # or")
    print("  sensor = DS18B20(sensor_id='2800000456789')  # Specific sensor")
    print("  temperature_c = sensor.read_temperature()")
    print("  temperature_f = sensor.read_temperature_fahrenheit()")
    print()
    print("Note: Requires 1-Wire interface and DS18B20 sensor")
    print()

def demo_sensors():
    """Demonstrate Sensors module usage"""
    print("=" * 50)
    print("Sensors Module Demo")
    print("=" * 50)
    print("Usage example:")
    print("  from src.sensors import SensorHub")
    print("  hub = SensorHub()")
    print("  status = hub.get_sensor_status()")
    print("  readings = hub.read_all()")
    print("  print(f\"Voltage: {readings['voltage']:.3f} V\")")
    print("  print(f\"Current: {readings['current']:.3f} A\")")
    print("  print(f\"Power: {readings['power']:.3f} W\")")
    print("  print(f\"Temperature: {readings['temperature']:.2f}°C\")")
    print("  hub.close()")
    print()
    print("Note: Combines readings from all sensors")
    print()

def demo_data_logger():
    """Demonstrate Data Logger module usage"""
    print("=" * 50)
    print("Data Logger Module Demo")
    print("=" * 50)
    print("Usage example:")
    print("  from src.data_logger import DataLogger")
    print("  logger = DataLogger(data_dir='./data/raw')")
    print("  logger.start_experiment('test_experiment_001')")
    print()
    print("  # Log readings")
    print("  readings = {")
    print("      'voltage': 12.5,")
    print("      'current': 0.842,")
    print("      'power': 10.53,")
    print("      'temperature': 31.5")
    print("  }")
    print("  logger.log_reading(readings)")
    print()
    print("  logger.stop_experiment()")
    print()
    print("Note: Saves timestamped sensor data to CSV files")
    print()

def demo_data_collection():
    """Demonstrate main data collection script usage"""
    print("=" * 50)
    print("Data Collection Script Demo")
    print("=" * 50)
    print("Usage examples:")
    print("  # Basic usage")
    print("  python src/data_collection.py --experiment-id test001")
    print()
    print("  # Custom interval and duration")
    print("  python src/data_collection.py --experiment-id flight_test --interval 0.5 --duration 300")
    print()
    print("  # Verbose output")
    print("  python src/data_collection.py --experiment-id debug_run --verbose")
    print()
    print("Arguments:")
    print("  --experiment-id  Identifier for this experiment (default: 'default')")
    print("  --interval       Sampling interval in seconds (default: 1.0)")
    print("  --duration       Duration to run in seconds (0 = run indefinitely)")
    print("  --data-dir       Directory to save CSV files")
    print("  --verbose        Enable verbose logging")
    print()
    print("Note: Main script that ties all modules together")
    print()

def main():
    """Run all demos"""
    print("PBL Project - Sensor Modules Demonstration")
    print("This demo shows how to use the sensor modules without actual hardware.\n")

    demo_ina219()
    demo_ds18b20()
    demo_sensors()
    demo_data_logger()
    demo_data_collection()

    print("=" * 50)
    print("Next Steps:")
    print("1. Connect your hardware (INA219, DS18B20, OLED to Raspberry Pi 5)")
    print("2. Enable required interfaces:")
    print("   - I2C: sudo raspi-config -> Interface Options -> I2C -> Enable")
    print("   - 1-Wire: sudo raspi-config -> Interface Options -> 1-Wire -> Enable")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Test individual modules:")
    print("   python src/ina219.py")
    print("   python src/ds18b20.py")
    print("5. Run data collection:")
    print("   python src/data_collection.py --experiment-id test001 --duration 60")
    print("=" * 50)

if __name__ == "__main__":
    main()