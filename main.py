#!/usr/bin/env python3
import sys
import threading
from led_effects import simple_pulse, simple_blink
from gpio_handler import read_counter, update_counter
from camera_uploader import capture_and_upload_image
import RPi.GPIO as GPIO
import atexit

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

def cleanup():
    from led_effects import pixels
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()

atexit.register(cleanup)

try:
    stop_event = threading.Event()
    led_thread = threading.Thread(target=simple_pulse, args=(stop_event,))
    led_thread.start()

    try:
        counter = read_counter() + 1
        update_counter(counter)
        capture_and_upload_image(counter)
    finally:
        stop_event.set()
        led_thread.join()
        simple_blink()
except KeyboardInterrupt:
    pass
