import subprocess

# Function to run the external program
def run_program():
    try:
        # Replace 'your_program.py' with the actual program you want to run
        subprocess.run(["python3", "/home/johnbrechbill/whiteboardgit/WhiteboardTest"])
    except Exception as e:
        print(f"Error running the program: {e}")

print("Press Enter to run the program (Ctrl+C to exit)...")

try:
    while True:
        # Wait for the user to press Enter
        input("Press Enter to simulate button press: ")
        print("Key pressed!")
        run_program()

except KeyboardInterrupt:
    print("Program stopped")

