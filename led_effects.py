#!/usr/bin/env python3

import sys
import time

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import neopixel
from config import PIXEL_PIN, NUM_PIXELS, BRIGHTNESS

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=False)

pixels.fill((0, 0, 0))
pixels.show()

def apply_brightness(color):
    return tuple(int(c * BRIGHTNESS) for c in color)

def set_color(color):
    pixels.fill(apply_brightness(color))
    pixels.show()

def simple_pulse(stop_event):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = 0

    while not stop_event.is_set():
        base_color = base_colors[color_index]
        for i in range(0, 256, 2):
            if stop_event.is_set(): return
            color = tuple(int(c * (i / 255.0)) for c in base_color)
            set_color(color)
            time.sleep(0.02)

        for i in range(255, -1, -2):
            if stop_event.is_set(): return
            color = tuple(int(c * (i / 255.0)) for c in base_color)
            set_color(color)
            time.sleep(0.02)

        color_index = (color_index + 1) % len(base_colors)

def simple_blink():
    for i in range(NUM_PIXELS):
        pixels[i] = apply_brightness((255, 255, 255))
        pixels.show()
        time.sleep(0.05)
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.show()
