import sys
import os
import time

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

# Initialize the NeoPixel strip
pixel_pin = board.D18  # GPIO 18
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

# Clear all pixels at start
pixels.fill((0, 0, 0))
pixels.show()

# Function to set brightness for all pixels
def set_brightness(brightness):
    brightness = max(0, min(255, brightness))  # Clamp to valid range
    pixels.fill((brightness, brightness, brightness))
    pixels.show()

try:
    while True:
        # Fade in
        for i in range(0, 256, 2):
            set_brightness(i)
            time.sleep(0.02)

        # Fade out
        for i in range(255, -1, -2):
            set_brightness(i)
            time.sleep(0.02)

except KeyboardInterrupt:
    # Clear pixels on exit
    pixels.fill((0, 0, 0))
    pixels.show()
