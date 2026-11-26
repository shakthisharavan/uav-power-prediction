# UAV Power Prediction

Edge AI power management for autonomous UAVs. This repo covers the data-collection stage: a Raspberry Pi 5 reads voltage, current, power and temperature from sensors and logs them to CSV. Those CSVs are the training data for a lightweight power-prediction model.

## Hardware

| Part | Measures | Connection |
|---|---|---|
| Raspberry Pi 5 | Runs the code | n/a |
| INA219 | Bus voltage, current, power | I2C, default address `0x40` |
| DS18B20 | Temperature | 1-Wire, needs a 4.7 kΩ pull-up on the data line |
| SSD1306 OLED (optional) | Live readout | I2C, default address `0x3C` |

## Setup

1. Enable I2C and 1-Wire, then reboot:
   ```bash
   sudo raspi-config   # Interface Options -> I2C -> Enable, 1-Wire -> Enable
   ```
2. Clone the repo and install dependencies:
   ```bash
   git clone https://github.com/shakthisharavan/uav-power-prediction.git
   cd uav-power-prediction
   pip install -r requirements.txt
   ```
   Only `smbus2` is needed for data collection. `Adafruit-SSD1306` and `Pillow` are for the OLED. `pandas`, `numpy`, `scikit-learn` and `joblib` are for model training on a laptop.

## Usage

Run all commands from the repo root. The scripts use package imports, so start them with `python -m`.

Collect data:
```bash
# 1 s interval, runs until Ctrl+C
python -m src.data_collection --experiment-id test001 --data-dir ./data/raw

# 0.5 s interval for 5 minutes
python -m src.data_collection --experiment-id test002 --interval 0.5 --duration 300 --data-dir ./data/raw

# Debug output
python -m src.data_collection --experiment-id test003 --data-dir ./data/raw --verbose
```

| Option | Default | Meaning |
|---|---|---|
| `--experiment-id` | `default` | Label written to every row |
| `--interval` | `1.0` | Seconds between samples |
| `--duration` | `0` | Seconds to run, `0` means until Ctrl+C |
| `--data-dir` | `/home/bates/PBL/data/raw` | Where CSV files go. Set this to a folder that exists on your machine |
| `--verbose`, `-v` | off | Debug logging |

Test one sensor at a time:
```bash
python -m src.ina219
python -m src.ds18b20
python -m src.oled
python -m src.sensors
```

Run the sensor test suite:
```bash
python -m src.test_sensors
```

`python demo.py` prints usage examples for each module.

## Output format

One CSV file per run, with these columns:

| Column | Unit | Source |
|---|---|---|
| `timestamp` | ISO 8601 | system clock |
| `experiment_id` | n/a | `--experiment-id` |
| `voltage_v` | V | INA219 |
| `current_a` | A | INA219 |
| `power_w` | W | INA219 |
| `temperature_c` | °C | DS18B20 |

## Project layout

```
src/
  ina219.py          INA219 driver
  ds18b20.py         DS18B20 driver
  oled.py            OLED driver
  sensors.py         SensorHub: reads all sensors together
  data_logger.py     CSV logging
  data_collection.py command-line collection script
  test_sensors.py    sensor tests
demo.py              usage examples
requirements.txt     dependencies
```

## Next steps

1. Collect several runs under different loads.
2. Copy the CSVs to a laptop and clean them.
3. Add features such as rolling averages and lags.
4. Compare lightweight models and pick one on accuracy versus resource use.
5. Deploy the chosen model to the Pi 5.

## Troubleshooting

- INA219 not found: run `i2cdetect -y 1` and check the address. Use `0x41` if the module's address jumper is set.
- DS18B20 not found: check the pull-up resistor, and confirm `ls /sys/bus/w1/devices/` lists a `28-...` device.
- Permission or directory error when logging: pass a `--data-dir` that exists and is writable.
- Sanity check readings before training: power should be close to voltage × current.

## License

MIT. See [LICENSE](LICENSE).
