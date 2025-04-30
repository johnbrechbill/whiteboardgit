import sys
import os
import time

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

# Initialize the NeoPixel
pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

# Function to set brightness of all pixels
def set_brightness(brightness):
    color = (brightness, brightness, brightness)
    for i in range(num_pixels):
        pixels[i] = color
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
    # Turn off all pixels on exit
    set_brightness(0)
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()
