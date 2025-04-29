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
num_pixels = 9  # Nine LEDs
led_strip = neopixel.NeoPixel(pixel_pin, num_pixels)

# Function to set pixel brightness
def set_brightness(brightness):
    color = (int(brightness), int(brightness), int(brightness))
    led_strip.fill(color)

# Turn on all LEDs (blue)
led_strip.fill((0, 0, 255))
time.sleep(0.5)

# Turn off all LEDs
led_strip.fill((0, 0, 0))
time.sleep(0.5)

# Clear all LEDs
led_strip.fill((0, 0, 0))
