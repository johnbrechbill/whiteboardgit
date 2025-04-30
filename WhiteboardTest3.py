#!/usr/bin/env python3

import sys
import os
import RPi.GPIO as GPIO
import threading

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import subprocess
import time
import board
import neopixel
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# --- Configuration ---
pixel_pin = board.D18
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False)

BUTTON_PIN = 23
last_file_file = "/home/johnbrechbill/whiteboard/last_file.txt"
counter_file = "/home/johnbrechbill/whiteboard/counter.txt"
identification_file = "/home/johnbrechbill/whiteboard/identification.txt"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# --- Pixel Control Threads ---
def pulse_pixels(stop_event):
    while not stop_event.is_set():
        for i in range(0, 256, 5):
            brightness = i
            for p in range(num_pixels):
                pixels[p] = (brightness, brightness, brightness)
            pixels.show()
            time.sleep(0.005)
            if stop_event.is_set():
                break
        for i in range(255, -1, -5):
            brightness = i
            for p in range(num_pixels):
                pixels[p] = (brightness, brightness, brightness)
            pixels.show()
            time.sleep(0.005)
            if stop_event.is_set():
                break
    clear_pixels()

def blink_pixels():
    for _ in range(3):
        for i in range(num_pixels):
            pixels[i] = (255, 255, 255)
        pixels.show()
        time.sleep(0.3)
        clear_pixels()
        time.sleep(0.2)

def clear_pixels():
    for i in range(num_pixels):
        pixels[i] = (0, 0, 0)
    pixels.show()

# --- Utility Functions ---
def read_counter():
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read().strip())
    return 0

def update_counter(counter):
    with open(counter_file, 'w') as file:
        file.write(str(counter))

def read_identification():
    if os.path.exists(identification_file):
        with open(identification_file, 'r') as file:
            return file.read().strip()
    return 'none'

def capture_and_upload_image(read_identification, counter, last_file_file):
    identification_prefix = read_identification()
    image_mark = f"{identification_prefix}{counter}"
    image_path = f"/home/johnbrechbill/whiteboard/{image_mark}.jpg"

    subprocess.run([
        "libcamera-still",
        "-o", image_path,
        "--autofocus-mode", "continuous",
        "--quality", "100",
        "--shutter", "200000",
        "--hdr", "auto",
    ])

    with open(last_file_file, 'w') as file:
        file.write(image_path)

    cloudinary.config(
        cloud_name="db6fegsqa",
        api_key="428688153637693",
        api_secret="nw2mtJx8oAVuxnTQmDxyDQ63we4"
    )

    response = cloudinary.uploader.upload(
        image_path,
        public_id=image_mark,
        upload_preset="PerspectiveAuto"
    )

    url, options = cloudinary_url(image_mark)
    print("Transformed Image URL:", url)
    return url

# --- Main Loop ---
print("Waiting for button press...")

if os.path.exists(last_file_file):
    with open(last_file_file, 'r') as file:
        last_image_path = file.read().strip()
    if os.path.exists(last_image_path):
        os.remove(last_image_path)

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button Pressed")

            stop_pulse = threading.Event()
            pulse_thread = threading.Thread(target=pulse_pixels, args=(stop_pulse,))
            pulse_thread.start()

            counter = read_counter() + 1
            update_counter(counter)

            def task():
                global result
                result = capture_and_upload_image(read_identification, counter, last_file_file)

            t = threading.Thread(target=task)
            t.start()

            while t.is_alive():
                time.sleep(0.1)

            stop_pulse.set()
            pulse_thread.join()

            t.join()
            print("Result:", result)

            blink_pixels()
            time.sleep(0.3)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped")
    clear_pixels()
    GPIO.cleanup()
