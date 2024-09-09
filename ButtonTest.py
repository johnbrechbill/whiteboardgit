import subprocess
import keyboard  # Make sure to install this with 'pip install keyboard'

# Function to run the external program
def run_program():
    try:
        # Replace 'your_program.py' with the actual program you want to run
        subprocess.run(["python3", "/path/to/your_program.py"])
    except Exception as e:
        print(f"Error running the program: {e}")

print("Press Enter to run the program (Ctrl+C to exit)...")

try:
    while True:
        # Check if Enter key is pressed
        if keyboard.is_pressed('enter'):
            print("Enter key pressed!")
            run_program()
            keyboard.wait('enter')  # Wait for another Enter press before proceeding

except KeyboardInterrupt:
    print("Program stopped")
