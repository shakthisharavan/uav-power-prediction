"""
Data Logger Module for Saving Sensor Data to CSV Files
"""

import csv
import os
import time
from datetime import datetime
from typing import Dict, Optional
import logging

class DataLogger:
    """
    Logger for saving sensor data to CSV files with timestamps
    """

    def __init__(self,
                 data_dir: str = "/home/bates/PBL/data/raw",
                 filename_prefix: str = "sensor_data",
                 auto_save_interval: int = 10):
        """
        Initialize data logger

        Args:
            data_dir: Directory to save CSV files
            filename_prefix: Prefix for CSV filenames
            auto_save_interval: Number of readings between auto-saves (for buffering)
        """
        self.logger = logging.getLogger(__name__)
        self.data_dir = data_dir
        self.filename_prefix = filename_prefix
        self.auto_save_interval = auto_save_interval

        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Buffer for readings before writing to disk
        self.buffer = []
        self.buffer_size = 0

        # CSV headers
        self.headers = [
            'timestamp',
            'experiment_id',
            'voltage_v',
            'current_a',
            'power_w',
            'temperature_c'
        ]

        # Current session info
        self.experiment_id = None
        self.session_start_time = None
        self.current_file = None
        self.csv_writer = None
        self.csv_file = None

        self.logger.info(f"DataLogger initialized. Saving to {self.data_dir}")

    def start_experiment(self, experiment_id: str):
        """
        Start a new experiment logging session

        Args:
            experiment_id: Identifier for this experiment
        """
        # Close any existing file
        self.close_current_file()

        self.experiment_id = experiment_id
        self.session_start_time = datetime.now()

        # Create filename with timestamp
        timestamp_str = self.session_start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.filename_prefix}_{experiment_id}_{timestamp_str}.csv"
        self.current_file = os.path.join(self.data_dir, filename)

        # Open file and write header
        try:
            self.csv_file = open(self.current_file, 'w', newline='')
            self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=self.headers)
            self.csv_writer.writeheader()
            self.logger.info(f"Started experiment '{experiment_id}'. Logging to {self.current_file}")
        except Exception as e:
            self.logger.error(f"Error opening log file {self.current_file}: {e}")
            self.csv_file = None
            self.csv_writer = None

    def log_reading(self, readings: Dict[str, float], experiment_id: Optional[str] = None):
        """
        Log a single sensor reading

        Args:
            readings: Dictionary containing sensor readings
            experiment_id: Optional experiment ID (uses current if not provided)
        """
        if experiment_id is not None and experiment_id != self.experiment_id:
            # If experiment ID changed, start new experiment
            self.start_experiment(experiment_id)

        # Prepare data row
        row = {
            'timestamp': datetime.now().isoformat(),
            'experiment_id': self.experiment_id or 'unknown',
            'voltage_v': readings.get('voltage', 0.0),
            'current_a': readings.get('current', 0.0),
            'power_w': readings.get('power', 0.0),
            'temperature_c': readings.get('temperature', 0.0)
        }

        # Add to buffer
        self.buffer.append(row)
        self.buffer_size += 1

        # Write to disk if buffer is full
        if self.buffer_size >= self.auto_save_interval:
            self.flush_buffer()

    def flush_buffer(self):
        """Write buffered readings to CSV file"""
        if not self.buffer or not self.csv_writer:
            return

        try:
            for row in self.buffer:
                self.csv_writer.writerow(row)
            self.csv_file.flush()  # Ensure data is written to disk
            self.logger.debug(f"Flushed {len(self.buffer)} readings to {self.current_file}")
            self.buffer.clear()
            self.buffer_size = 0
        except Exception as e:
            self.logger.error(f"Error flushing buffer to {self.current_file}: {e}")

    def close_current_file(self):
        """Close the current CSV file"""
        if self.csv_file:
            try:
                self.flush_buffer()  # Write any remaining buffered data
                self.csv_file.close()
                self.logger.info(f"Closed log file: {self.current_file}")
            except Exception as e:
                self.logger.error(f"Error closing log file {self.current_file}: {e}")
            finally:
                self.csv_file = None
                self.csv_writer = None
                self.buffer.clear()
                self.buffer_size = 0

    def stop_experiment(self):
        """Stop the current experiment and close the file"""
        if self.experiment_id:
            self.logger.info(f"Stopping experiment '{self.experiment_id}'")
        self.close_current_file()
        self.experiment_id = None
        self.session_start_time = None

    def get_log_file_size(self) -> int:
        """
        Get size of current log file in bytes

        Returns:
            File size in bytes, or 0 if no file is open
        """
        if self.current_file and os.path.exists(self.current_file):
            return os.path.getsize(self.current_file)
        return 0

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = DataLogger(auto_save_interval=5)  # Flush every 5 readings for demo

    try:
        # Start an experiment
        logger.start_experiment("test_experiment_001")

        # Log some sample data
        import random
        for i in range(20):
            readings = {
                'voltage': 12.0 + random.uniform(-0.5, 0.5),
                'current': 0.5 + random.uniform(-0.1, 0.1),
                'temperature': 25.0 + random.uniform(-2, 2)
            }
            readings['power'] = readings['voltage'] * readings['current']  # Calculate power

            logger.log_reading(readings)
            print(f"Logged reading {i+1}: V={readings['voltage']:.2f}, I={readings['current']:.3f}, "
                  f"P={readings['power']:.2f}, T={readings['temperature']:.1f}°C")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopping logger...")
    finally:
        logger.stop_experiment()
        print(f"Log file size: {logger.get_log_file_size()} bytes")