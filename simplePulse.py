import sys
import os
import time

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

# Initialize the NeoPixel
pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 1  # One LED
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)  # Disable auto_write for better control

# Function to set pixel brightness
def set_brightness(brightness):
    pixels[0] = (brightness, brightness, brightness)  # Set the brightness for all color channels
    pixels.show()  # Update the LED after setting the brightness

# Fade in quickly
for i in range(0, 256, 5):  # Quick fade in (0 to 255 brightness)
    set_brightness(i)
    time.sleep(0.005)  # Adjust to make the fade-in fast

# Fade out slowly
for i in range(255, -1, -2):  # Slow fade out
    set_brightness(i)
    time.sleep(0.02)  # Adjust to make the fade-out slow

# Clear all pixels (turn off all LEDs)
pixels[0] = (0, 0, 0)
