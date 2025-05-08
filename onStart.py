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

# Set up SSH agent (note: might not be necessary in this script context)
subprocess.run("eval $(ssh-agent -s)", shell=True)
subprocess.run("ssh-add ~/.ssh/id_ed25519", shell=True)

# NeoPixel setup
pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# GPIO setup
BUTTON_PIN = 23  # BCM pin number
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

test_script = "/home/johnbrechbill/whiteboardgit/main.py"

# Function to run external script and stream output
def run_script(script_name):
    try:
        process = subprocess.Popen(
            ['python3', script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True  # equivalent to text=True in Python 3.7+
        )
        for line in process.stdout:
            print(line, end='')  # stream each line to terminal
        process.wait()
        return f"{script_name} exited with code {process.returncode}"
    except Exception as e:
        return f"Failed to run {script_name}: {e}"

print("Waiting for button press...")

try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button Pressed")
            output = run_script(test_script)
            print(output)
            time.sleep(2)  # debounce
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()
