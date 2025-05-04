import sys
import os
import RPi.GPIO as GPIO
import subprocess
import time

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import board
import neopixel

pixel_pin = board.D18
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

BUTTON_PIN = 23
test_script = "/home/johnbrechbill/whiteboardgit/WhiteboardTest3.py"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def run_script(script_name):
    try:
        result = subprocess.run(['python3', script_name], capture_output=True, text=True, check=True)
        print(f"{script_name} succeeded:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{script_name} failed with return code {e.returncode}:\n{e.stderr}")

def button_callback(channel):
    print("Button Pressed")
    run_script(test_script)

# Detect falling edge with debounce (200ms)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

print("Waiting for button press... Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(1)  # Idle loop; program will respond via callback
except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()
