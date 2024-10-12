import sys
import os
import RPi.GPIO as GPIO
import subprocess
import time

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 1  # One LED
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# GPIO setup
BUTTON_PIN = 23  # Pin 23 for the button

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin 23 as input with pull-up resistor

# Function to run the whiteboard program
def run_upload():
    try:
        subprocess.run(["python3", "/home/johnbrechbill/whiteboardgit/WhiteboardTest.py"])
    except Exception as e:
        print(f"Error running the WhiteboardTest program: {e}")

# Function to run the simpleBlink program
def run_blink():
    try:
        # Use Popen instead of run to prevent blocking
        subprocess.Popen(["python3", "/home/johnbrechbill/whiteboardgit/simpleBlink.py"])
    except Exception as e:
        print(f"Error running the simpleBlink program: {e}")

print("Waiting for button press...")

def run_pulse():
    try:
        # Use Popen instead of run to prevent blocking
        subprocess.Popen(["python3", "/home/johnbrechbill/whiteboardgit/simplePulse.py"])
    except Exception as e:
        print(f"Error running the simplePulse program: {e}")

try:
    while True:
        # Wait for the button press (button will pull the pin to LOW when pressed)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed!")
            run_pulse()
            run_upload()  # Run the WhiteboardTest.py script
            run_blink()
            time.sleep(0.2)  # Debounce delay to prevent multiple detections
        # Continue looping and checking for the next button press
        time.sleep(0.1)  # Small delay to prevent high CPU usage in the loop

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
