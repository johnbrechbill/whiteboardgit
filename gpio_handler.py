import os
import RPi.GPIO as GPIO
from config import COUNTER_FILE, IDENTIFICATION_FILE, BUTTON_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as file:
            return int(file.read().strip())
    return 0

def update_counter(counter):
    with open(COUNTER_FILE, 'w') as file:
        file.write(str(counter))

def read_identification():
    if os.path.exists(IDENTIFICATION_FILE):
        with open(IDENTIFICATION_FILE, 'r') as file:
            return file.read().strip()
    return 'none'
