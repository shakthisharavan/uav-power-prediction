"""
Main Data Collection Script for Reading Sensors and Logging to CSV
"""

import time
import argparse
import signal
import sys
from typing import Dict
import logging

from .sensors import SensorHub
from .data_logger import DataLogger

# Global flag for graceful shutdown
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C for graceful shutdown"""
    global running
    print("\nReceived interrupt signal. Shutting down gracefully...")
    running = False

def main():
    """Main data collection function"""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Collect sensor data from INA219 and DS18B20')
    parser.add_argument('--experiment-id', type=str, default='default',
                        help='Identifier for this experiment')
    parser.add_argument('--interval', type=float, default=1.0,
                        help='Sampling interval in seconds (default: 1.0)')
    parser.add_argument('--duration', type=int, default=0,
                        help='Duration to run in seconds (0 = run indefinitely)')
    parser.add_argument('--data-dir', type=str, default='/home/bates/PBL/data/raw',
                        help='Directory to save CSV files')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Initialize sensor hub and data logger
        logger.info("Initializing sensors...")
        sensor_hub = SensorHub()

        logger.info("Initializing data logger...")
        data_logger = DataLogger(data_dir=args.data_dir)

        # Start experiment
        data_logger.start_experiment(args.experiment_id)

        logger.info(f"Starting data collection for experiment '{args.experiment_id}'")
        logger.info(f"Sampling interval: {args.interval} seconds")
        if args.duration > 0:
            logger.info(f"Duration: {args.duration} seconds")
        else:
            logger.info("Duration: indefinite (press Ctrl+C to stop)")
        logger.info("-" * 50)

        start_time = time.time()
        sample_count = 0

        # Main data collection loop
        while running and (args.duration == 0 or (time.time() - start_time) < args.duration):
            loop_start = time.time()

            # Read all sensors
            readings = sensor_hub.read_all()

            # Log the readings
            data_logger.log_reading(readings, args.experiment_id)

            # Display readings
            print(f"Sample {sample_count + 1:4d} | "
                  f"V: {readings['voltage']:6.3f} V | "
                  f"I: {readings['current']:6.3f} A | "
                  f"P: {readings['power']:6.3f} W | "
                  f"T: {readings['temperature']:5.1f}°C")

            sample_count += 1

            # Calculate sleep time to maintain interval
            loop_time = time.time() - loop_start
            sleep_time = max(0, args.interval - loop_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

        # Final statistics
        elapsed_time = time.time() - start_time
        logger.info("-" * 50)
        logger.info(f"Data collection completed.")
        logger.info(f"Experiment ID: {args.experiment_id}")
        logger.info(f"Samples collected: {sample_count}")
        logger.info(f"Elapsed time: {elapsed_time:.1f} seconds")
        if elapsed_time > 0:
            logger.info(f"Average sampling rate: {sample_count/elapsed_time:.2f} Hz")
        logger.info(f"Log file size: {data_logger.get_log_file_size()} bytes")

    except Exception as e:
        logger.error(f"Error in data collection: {e}", exc_info=True)
        sys.exit(1)

    finally:
        # Clean up
        logger.info("Cleaning up resources...")
        try:
            data_logger.stop_experiment()
        except Exception as e:
            logger.error(f"Error stopping data logger: {e}")

        try:
            sensor_hub.close()
        except Exception as e:
            logger.error(f"Error closing sensor hub: {e}")

        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()