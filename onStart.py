#!/usr/bin/env python3

import sys
import os
import RPi.GPIO as GPIO
import subprocess
import time

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel
import concurrent.futures

subprocess.run("eval $(ssh-agent -s)", shell=True)
subprocess.run("ssh-add ~/.ssh/id_ed25519", shell=True)

pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 9  # One LED
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# GPIO setup
BUTTON_PIN = 23  # Pin 23 for the button

test_script="/home/johnbrechbill/whiteboardgit/WhiteboardTest3.py"

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin 23 as input with pull-up resistor


# Test Function To Run Script
def run_script(script_name):
    try:
        result = subprocess.Popen(['python3', script_name], capture_output=True, text=True, check=True)
        return f"{script_name} succeeded:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"{script_name} failed with return code {e.returncode}:\n{e.stderr}"

print("Waiting for button press...")

try:
    while True:
        # Wait for the button press (button will pull the pin to LOW when pressed)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button Pressed")
            run_script(test_script)
            output = run_script(test_script)
            print(output)
            time.sleep(2)  # Debounce delay to prevent multiple detections
            # Continue looping and checking for the next button press
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
