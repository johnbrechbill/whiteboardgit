import sys
import os
import RPi.GPIO as GPIO
import subprocess
import time

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

# GPIO setup
BUTTON_PIN = 23  # Pin 23 for the button

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set pin 23 as input with pull-up resistor

# Function to run the external program
def run_program():
    try:
        # Replace with the actual program you want to run
        subprocess.run(["python3", "/home/johnbrechbill/whiteboardgit/WhiteboardTest.py"])
    except Exception as e:
        print(f"Error running the program: {e}")

print("Waiting for button press...")

try:
    while True:
        # Wait for the button press (button will pull the pin to LOW when pressed)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed!")
            run_program()
            time.sleep(0.2)  # Debounce delay to prevent multiple detections
        # Continue looping and checking for the next button press
        time.sleep(0.1)  # Small delay to prevent high CPU usage in the loop

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO settings on exit
