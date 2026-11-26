# PBL Project: Edge AI-Based Predictive Power Management for Autonomous UAVs

This repository contains the software implementation for an edge AI UAV power management system. The system collects sensor data from INA219 (voltage/current/power) and DS18B20 (temperature) sensors on a Raspberry Pi 5, logs the data to CSV files, and provides a foundation for machine learning model training and deployment.

## Project Structure

```
PBL/
├── data/
│   ├── raw/          # Raw CSV data from sensors
│   └── processed/    # Cleaned and featured datasets (for ML processing
├── docs/             # Documentation
├── models/           # Trained ML models
└── src/              # Source code
    ├── ina219.py         # INA219 sensor driver
    ├── ds18b20.py        # DS18B20 temperature sensor driver
    ├── oled.py           # OLED display driver
    ├── sensors.py        # Sensor fusion module
    ├── data_logger.py    # CSV logging functionality
    └── data_collection.py # Main data collection script
```

## Installation

1. Install required dependencies:
   ```bash
   pip install smbus2
   ```

2. Enable required kernel modules:
   ```bash
   # For I2C (INA219)
   sudo modprobe i2c-dev
   
   # For 1-Wire (DS18B20)
   sudo modprobe w1-gpio
   sudo modprobe w1-therm
   ```

3. For OLED display (optional):
   ```bash
   pip install Adafruit-SSD1306
   ```

## Usage

### Data Collection

The main script for collecting sensor data is `src/data_collection.py`:

```bash
# Basic usage - collect data indefinitely with 1-second interval
python src/data_collection.py --experiment-id test001

# Specify sampling interval and duration
python src/data_collection.py --experiment-id test002 --interval 0.5 --duration 300

# Verbose output for debugging
python src/data_collection.py --experiment-id test003 --verbose
```

### Individual Sensor Testing

Test INA219 sensor:
```bash
python src/ina219.py
```

Test DS18B20 sensor:
```bash
python src/ds18b20.py
```

Test OLED display:
```bash
python src/oled.py
```

Test sensor fusion:
```bash
python src/sensors.py
```

## Data Format

CSV files are saved in `/home/bates/PBL/data/raw/` with the following columns:
- `timestamp`: ISO format timestamp
- `experiment_id`: Identifier for the experiment
- `voltage_v`: Bus voltage in volts (from INA219)
- `current_a`: Current in amperes (from INA219)
- `power_w`: Power in watts (from INA219)
- `temperature_c`: Temperature in Celsius (from DS18B20)

## Next Steps

After collecting sufficient data:
1. Transfer CSV files to your laptop for processing
2. Clean and preprocess the dataset
3. Perform feature engineering (calculate temporal features, lag features, etc.)
4. Train and compare lightweight ML models
5. Select optimal model based on accuracy/resource trade-off
6. Deploy selected model back to Raspberry Pi 5

## Notes

- Ensure proper hardware connections before running the software
- The INA219 default address is 0x40, but this can vary based on module configuration
- The DS18B20 sensor requires 4.7k pull-up resistor on the data line
- Always validate sensor readings for reasonableness before proceeding to ML training