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

# Function to set brightness for all pixels
def set_brightness(brightness):
    brightness = max(0, min(255, brightness))  # Clamp to valid range
    pixels.fill((brightness, brightness, brightness))
    pixels.show()

def led_animation(stop_event):
    while not stop_event.is_set():
        for i in range(0, 256, 2):
            if stop_event.is_set(): break
            set_brightness(i)
            time.sleep(0.02)
        for i in range(255, -1, -2):
            set_brightness(i)
            time.sleep(0.02)

#GPIO setup
BUTTON_PIN = 23  # Pin 23 for the button

blink_script="/home/johnbrechbill/whiteboardgit/simpleBlink.py"
last_file_file = "/home/johnbrechbill/whiteboard/last_file.txt"
counter_file = "/home/johnbrechbill/whiteboard/counter.txt"
identification_file = "/home/johnbrechbill/whiteboard/identification.txt"

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin 23 as input with pull-up resistor

# Test Function To Run Script
def run_script(script_name):
    try:
        result = subprocess.run(['python3', script_name], capture_output=True, text=True, check=True)
        return f"{script_name} succeeded:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"{script_name} failed with return code {e.returncode}:\n{e.stderr}"

# Function to read the current counter value
def read_counter():
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read().strip())
    return 0  # Start at 0 if the file doesn't exist

# Function to update the counter value
def update_counter(counter):
    with open(counter_file, 'w') as file:
        file.write(str(counter))

# Increment the counter
counter = read_counter() + 1
update_counter(counter)

# Function to read the identification prefix
def read_identification():
    if os.path.exists(identification_file):
        with open(identification_file, 'r') as file:
            return file.read().strip()
    return 'none'  # Default prefix if the file doesn't exist

def capture_and_upload_image(counter, last_file_file):
    print("capture and upload image processing...")
    # Read the identification prefix
    identification_prefix = read_identification()

    print("read identification prefix")
    
    # Format the counter with leading zeros (e.g., a001, a002, etc.)
    image_mark = f"{identification_prefix}{counter}"

    print("image marked")

    # Image path where the flipped image will be stored
    image_path = f"/home/johnbrechbill/whiteboard/{image_mark}.jpg"

    # Run libcamera-still with adjusted quality and shutter speed
    subprocess.run([
        "libcamera-still",
        "-o", image_path,
        "--autofocus-mode", "continuous",
        "--quality", "100",             # Set JPEG quality to maximum
        "--shutter", "200000",
        "--hdr", "auto",
    ])

    print("ran subprocess")

    # Save the current image path as the last file
    with open(last_file_file, 'w') as file:
        file.write(image_path)

    print("wrote to file")

    # Cloudinary configuration
    cloudinary.config(
        cloud_name="db6fegsqa",
        api_key="428688153637693",
        api_secret="nw2mtJx8oAVuxnTQmDxyDQ63we4"
    )

    # Upload the image with the preset effect
    response = cloudinary.uploader.upload(
        image_path,
        public_id=image_mark,
        upload_preset="PerspectiveAuto"
    )

    print("uploaded image")

    # Get the URL of the transformed image
    url, options = cloudinary_url(image_mark)

    print("Transformed Image URL:", url)
    return url
    
# Delete the previous file if it exists
if os.path.exists(last_file_file):
    with open(last_file_file, 'r') as file:
        last_image_path = file.read().strip()
    if os.path.exists(last_image_path):
        os.remove(last_image_path)
try:
    while True:
        stop_event = threading.Event()
        led_thread = threading.Thread(target=led_animation, args=(stop_event,))
        led_thread.start()
    
        try:
            capture_and_upload_image(counter, last_file_file)
        finally:
            stop_event.set()
            led_thread.join()
            run_script(blink_script)
except KeyboardInterrupt:
    GPIO.cleanup()
