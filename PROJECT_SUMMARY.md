# PBL Project Summary

## Overview
This project implements the software workflow for an edge AI UAV power management system. The system collects sensor data from INA219 (voltage/current/power) and DS18B20 (temperature) sensors on a Raspberry Pi 5, logs the data to CSV files, and provides a foundation for machine learning model training and deployment.

## What We've Built

### Core Sensor Modules
1. **`src/ina219.py`** - Driver for INA219 current/power monitor over I2C
2. **`src/ds18b20.py`** - Driver for DS18B20 temperature sensor over 1-Wire
3. **`src/oled.py`** - Driver for SSD1306-based OLED display over I2C
4. **`src/sensors.py`** - Sensor fusion module combining readings from all sensors
5. **`src/data_logger.py`** - CSV logging functionality with timestamped experiment tracking
6. **`src/data_collection.py`** - Main script that ties all modules together for continuous data collection

### Supporting Files
- **`src/test_sensors.py`** - Test suite for verifying module functionality
- **`src/demo.py`** - Demonstration script showing usage examples
- **`README.md`** - Project overview and usage instructions
- **`requirements.txt`** - Python dependencies
- **`configs/data_collection.yaml`** - Configuration template
- **`PROJECT_SUMMARY.md`** - This file

## Project Structure
```
PBL/
├── data/
│   ├── raw/          # Raw CSV data from sensors
│   └── processed/    # Cleaned and featured datasets (for ML processing)
├── docs/             # Documentation (place for papers, schematics, etc.)
├── models/           # Trained ML models (to be created during ML phase)
├── configs/          # Configuration files
│   └── data_collection.yaml
├── src/              # Source code
│   ├── ina219.py
│   ├── ds18b20.py
│   ├── oled.py
│   ├── sensors.py
│   ├── data_logger.py
│   ├── data_collection.py
│   ├── test_sensors.py
│   └── demo.py
├── README.md
├── requirements.txt
└── PROJECT_SUMMARY.md
```

## Immediate Next Steps (Phase 1: Data Collection)
Based on the project plan, the immediate software objective is:
> **"Get reliable CSV data from INA219 + DS18B20 on the Pi 5."**

To achieve this:

1. **Hardware Setup** (User indicated this is complete):
   - Raspberry Pi 5 8GB connected to power supply
   - INA219 connected via I2C (typically address 0x40)
   - DS18B20 connected via 1-Wire with 4.7k pull-up resistor
   - OLED display connected via I2C (optional, typically address 0x3C)

2. **Software Installation**:
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Enable required interfaces (run once)
   sudo raspi-config
   # -> Interface Options -> I2C -> Enable
   # -> Interface Options -> 1-Wire -> Enable
   # Reboot after enabling interfaces
   ```

3. **Test Individual Modules**:
   ```bash
   # Test INA219
   python src/ina219.py
   
   # Test DS18B20
   python src/ds18b20.py
   
   # Test OLED (if connected)
   python src/oled.py
   
   # Test sensor fusion
   python src/sensors.py
   ```

4. **Start Data Collection**:
   ```bash
   # Collect data for 5 minutes with 1-second intervals
   python src/data_collection.py --experiment-id test001 --duration 300
   
   # Collect data indefinitely (stop with Ctrl+C)
   python src/data_collection.py --experiment-id ongoing_test
   
   # Verbose output for debugging
   python src/data_collection.py --experiment-id debug_run --verbose
   ```

## Data Format
CSV files are saved in `/home/bates/PBL/data/raw/` with columns:
- `timestamp`: ISO format timestamp (e.g., "2026-09-24T10:30:45.123456")
- `experiment_id`: Identifier for the experiment (from --experiment-id argument)
- `voltage_v`: Bus voltage in volts (from INA219)
- `current_a`: Current in amperes (from INA219)
- `power_w`: Power in watts (from INA219)
- `temperature_c`: Temperature in Celsius (from DS18B20)

## Transition to ML Workflow
Once reliable data collection is established (multiple datasets under different load conditions), proceed to:

1. **Data Transfer**: Copy CSV files from Raspberry Pi to laptop for processing
2. **Data Cleaning**: Remove invalid readings, handle missing values, filter outliers
3. **Feature Engineering**: Calculate temporal features (rates, rolling averages, lags)
4. **Model Training**: Compare lightweight models (Linear Regression, Decision Tree, Random Forest, Gradient Boosting)
5. **Model Selection**: Choose based on accuracy/resource trade-off (not just accuracy)
6. **Deployment**: Export selected model and deploy back to Raspberry Pi 5 for edge inference

## Verification Criteria
The data collection phase is complete when:
1. Raspberry Pi 5 reliably reads from both INA219 and DS18B20 sensors
2. Data is logged to CSV with correct timestamps and plausible values
3. Multiple datasets have been collected under different load conditions
4. Data passes basic validation:
   - Timestamps are monotonic
   - No impossible negative/out-of-range values
   - Power ≈ Voltage × Current (within measurement error)
   - Reasonable sampling consistency

## Notes for Future Sessions
- This project has been set up with the name "PBL project" for easy recall in future sessions
- All source code is in `/home/bates/PBL/src/`
- Data is stored in `/home/bates/PBL/data/`
- Configurations are in `/home/bates/PBL/configs/`
- To resume work in future sessions, simply navigate to `/home/bates/PBL/` and continue
- The claude-mem system will help maintain context across sessions

## References
See the detailed plan in `/home/bates/.claude/plans/dapper-petting-frog.md` for the complete implementation roadmap including ML training, model selection, edge deployment, and validation steps.