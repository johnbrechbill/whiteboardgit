#!/usr/bin/env python3

import sys
import os
import RPi.GPIO as GPIO
import threading

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import subprocess
import time
import board
import neopixel
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configure the NeoPixel
pixel_pin = board.D18  
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

# Global brightness multiplier (0.0 to 1.0)
BRIGHTNESS = 0.8  # Adjust this to control overall brightness

# Clear any existing LED state on startup
pixels.fill((0, 0, 0))
pixels.show()

# Function to apply global brightness
def apply_brightness(color):
    return tuple(int(c * BRIGHTNESS) for c in color)

# Function to set all pixels to a single RGB color, with brightness applied
def set_color(color):
    pixels.fill(apply_brightness(color))
    pixels.show()

def simple_pulse():
    base_colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
    ]
    color_index = 0

    base_color = base_colors[color_index]
        
    # Fade in
    for i in range(0, 256, 2):
        scale = i / 255.0
        color = tuple(int(c * scale) for c in base_color)
        set_color(color)
        time.sleep(0.02)
    
    # Fade out
    for i in range(255, -1, -2):
        scale = i / 255.0
        color = tuple(int(c * scale) for c in base_color)
        set_color(color)
        time.sleep(0.02)

    color_index = (color_index + 1) % len(base_colors)

def simple_blink():    
    # Zoom across: progressively light more pixels
    for i in range(num_pixels):
        pixels[i] = apply_brightness((255, 255, 255))  # Light the next pixel
        pixels.show()
        time.sleep(0.05)
    
    # Hold full-on state for half a second
    time.sleep(0.5)
    
    # Turn all pixels off
    pixels.fill((0, 0, 0))
    pixels.show()


simple_pulse()
simple_blink()
