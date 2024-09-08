import RPi.GPIO as GPIO
import subprocess
import time

# Set up the GPIO pin for the button (using GPIO pin 17)
BUTTON_PIN = 17

# Function to run the external program
def run_program():
    try:
        # Replace 'your_program.py' with the actual program you want to run
        subprocess.run(["python3", "/path/to/your_program.py"])
    except Exception as e:
        print(f"Error running the program: {e}")

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button pin set as input with pull-up resistor

print("Waiting for button press...")

try:
    while True:
        # Detect button press (button pin will go low when pressed)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Button pressed!")
            run_program()
            time.sleep(0.2)  # Debounce delay
        time.sleep(0.1)  # Small delay to prevent high CPU usage

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
