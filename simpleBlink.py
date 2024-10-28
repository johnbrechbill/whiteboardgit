import sys
import os
import RPi.GPIO as GPIO
import subprocess
import time


sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 1  # One LED
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# Function to set pixel brightness
def set_brightness(brightness):
    # Set the pixel color (in RGB format). You can change the color if desired.
    pixels[0] = (int(brightness), int(brightness), int(brightness))

# Turn on the LED (white)
pixels[0] = (0, 255, 0)
time.sleep(.5)  # Keep it on for 1 second

# Turn off the LED
pixels[0] = (0, 0, 0)
time.sleep(.5)  # Keep it off for 1 second

# Clear all pixels (turn off all LEDs)
pixels.fill((0, 0, 0))
