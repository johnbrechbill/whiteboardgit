#!/usr/bin/env python3
import sys
import os
import subprocess
import time
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')
import board
import neopixel

# Set up SSH agent (note: might not be necessary in this script context)
subprocess.run("eval $(ssh-agent -s)", shell=True)
subprocess.run("ssh-add ~/.ssh/id_ed25519", shell=True)

# NeoPixel setup
pixel_pin = board.D18  # GPIO 18 (physical pin 12)
num_pixels = 9
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

test_script = "/home/johnbrechbill/whiteboardgit/WhiteboardTest3.py"

# Function to run external script and stream output
def run_script(script_name):
    try:
        process = subprocess.Popen(
            ['python3', script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        return f"{script_name} exited with code {process.returncode}"
    except Exception as e:
        return f"Failed to run {script_name}: {e}"

print("Starting automated photo capture every 2 hours...")

try:
    while True:
        print(f"Running script at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        output = run_script(test_script)
        print(output)
        
        # Wait 2 hours (7200 seconds)
        print("Waiting 2 hours until next capture...")
        time.sleep(7200)
        
except KeyboardInterrupt:
    print("Program stopped")
