import sys
import os
import time

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

# Initialize the NeoPixel strip
pixel_pin = board.D18
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

# Ensure all pixels start off
pixels.fill((0, 0, 0))
pixels.show()

# Define zoom color
color = (255, 255, 255)

# Zoom across: progressively light more pixels
for i in range(num_pixels):
    pixels[i] = color  # Light the next pixel
    pixels.show()      # Update the strip
    time.sleep(0.05)   # Speed of zooming

# Hold full-on state for half a second
time.sleep(0.5)

# Turn all pixels off
pixels.fill((0, 0, 0))
pixels.show()
