

import sys
import os

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import subprocess

# Function to run the external program
def run_program():
    try:
        # Replace 'your_program.py' with the actual program you want to run
        subprocess.run(["python3", "/home/johnbrechbill/whiteboardgit/WhiteboardTest.py"])
    except Exception as e:
        print(f"Error running the program: {e}")

print("Running the program...")

try:
    # Automatically run the external program when this script is executed
    run_program()

except KeyboardInterrupt:
    print("Program stopped")
