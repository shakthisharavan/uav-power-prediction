"""
OLED Display Module for Showing Sensor Data
"""

import logging
from typing import Optional

# Try to import OLED libraries, but provide fallbacks if not available
try:
    import Adafruit_SSD1306
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    OLED_AVAILABLE = True
except ImportError:
    OLED_AVAILABLE = False
    logging.warning("OLED libraries not available. Running in simulation mode.")

class OLEDDisplay:
    """
    Driver for OLED display (typically SSD1306 based)
    """

    def __init__(self, width: int = 128, height: int = 64, i2c_address: int = 0x3C):
        """
        Initialize OLED display

        Args:
            width: Display width in pixels (default: 128)
            height: Display height in pixels (default: 64)
            i2c_address: I2C address of OLED (default: 0x3C)
        """
        self.logger = logging.getLogger(__name__)
        self.width = width
        self.height = height
        self.i2c_address = i2c_address

        if OLED_AVAILABLE:
            try:
                # Initialize display
                self.display = Adafruit_SSD1306.SSD1306_128_64(rst=None, i2c_address=i2c_address)
                self.display.begin()
                self.display.clear()
                self.display.display()

                # Create blank image for drawing
                self.image = Image.new('1', (width, height))
                self.draw = ImageDraw.Draw(self.image)

                # Load default font
                self.font = ImageFont.load_default()

                self.logger.info(f"OLED display initialized: {width}x{height} at address 0x{i2c_address:02x}")
            except Exception as e:
                self.logger.error(f"Failed to initialize OLED display: {e}")
                self.display = None
        else:
            self.display = None
            self.logger.info("OLED running in simulation mode")

    def clear(self):
        """Clear the display"""
        if self.display:
            self.display.clear()
            self.display.display()
        else:
            self.logger.debug("OLED clear (simulated)")

    def display_text(self, lines: list):
        """
        Display text lines on the OLED

        Args:
            lines: List of strings to display (one per line)
        """
        if self.display:
            try:
                # Clear image
                self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

                # Draw each line of text
                y_offset = 0
                line_height = 10  # Approximate line height
                for line in lines:
                    if y_offset < self.height:
                        self.draw.text((0, y_offset), str(line), font=self.font, fill=255)
                        y_offset += line_height

                # Display image
                self.display.image(self.image)
                self.display.display()
            except Exception as e:
                self.logger.error(f"Error displaying text on OLED: {e}")
        else:
            # Simulation mode - just log what would be displayed
            self.logger.info("OLED Display (simulated):")
            for i, line in enumerate(lines):
                self.logger.info(f"  Line {i}: {line}")

    def display_sensor_data(self, voltage: float, current: float, power: float, temperature: float):
        """
        Display sensor data in a formatted way

        Args:
            voltage: Voltage in volts
            current: Current in amperes
            power: Power in watts
            temperature: Temperature in Celsius
        """
        lines = [
            f"Voltage: {voltage:.2f} V",
            f"Current: {current:.3f} A",
            f"Power: {power:.2f} W",
            f"Temp: {temperature:.1f} C"
        ]
        self.display_text(lines)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    display = OLEDDisplay()

    try:
        # Show some test data
        display.display_sensor_data(12.5, 0.842, 10.53, 31.5)
        time.sleep(2)

        # Show some text
        display.display_text(["Hello", "World", "OLED", "Test"])
        time.sleep(2)

        # Clear display
        display.clear()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        display.clear()