import sys
import os
import RPi.GPIO as GPIO
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

# Fade in quickly
for i in range(0, 256, 5):  # Quick fade in (0 to 255 brightness)
    set_brightness(i)
    time.sleep(0.005)  # Adjust to make the fade-in fast

# Fade out slowly
for i in range(255, -1, -2):  # Slow fade out
    set_brightness(i)
    time.sleep(0.02)  # Adjust to make the fade-out slow

# Turn off the LED after the fade-out
pixels.fill((0, 0, 0))
