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

# Clear all pixels before starting
pixels.fill((0, 0, 0))
pixels.show()

# Define the color to zoom with
color = (0, 0, 255)  # Bright white

# Zoom effect: light up one more pixel in each step
for i in range(num_pixels):
    for j in range(i + 1):
        pixels[j] = color
    pixels.show()
    time.sleep(0.05)  # Adjust speed of "zoom"

# Hold full brightness for half a second
time.sleep(.2)

# Turn everything off
pixels.fill((0, 0, 0))
pixels.show()
