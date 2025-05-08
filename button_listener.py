import RPi.GPIO as GPIO
import subprocess
import time
from config import BUTTON_PIN

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup_gpio():
    GPIO.cleanup()

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

def wait_for_button(script_to_run):
    print("Waiting for button press...")
    try:
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                print("Button pressed")
                output = run_script(script_to_run)
                print(output)
                time.sleep(2)  # debounce
    except KeyboardInterrupt:
        print("Program stopped")
    finally:
        cleanup_gpio()
