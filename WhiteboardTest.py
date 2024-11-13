import sys
import os

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

import subprocess
import time
import board
import neopixel
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Configure the NeoPixel
pixel_pin = board.D18  
num_pixels = 1
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

last_file_file = "/home/johnbrechbill/whiteboard/last_file.txt"

# File path for storing the counter
counter_file = "/home/johnbrechbill/whiteboard/counter.txt"

# Function to read the current counter value
def read_counter():
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            return int(file.read().strip())
    return 0  # Start at 0 if the file doesn't exist

# Function to update the counter value
def update_counter(counter):
    with open(counter_file, 'w') as file:
        file.write(str(counter))

# Increment the counter
counter = read_counter() + 1
update_counter(counter)

identification_file = "/home/johnbrechbill/whiteboard/identification.txt"

# Function to read the identification prefix
def read_identification():
    if os.path.exists(identification_file):
        with open(identification_file, 'r') as file:
            return file.read().strip()
    return 'a'  # Default prefix if the file doesn't exist

# Delete the previous file if it exists
if os.path.exists(last_file_file):
    with open(last_file_file, 'r') as file:
        last_image_path = file.read().strip()
    if os.path.exists(last_image_path):
        os.remove(last_image_path)

# Read the identification prefix
identification_prefix = read_identification()

# Format the counter with leading zeros (e.g., a001, a002, ..., a000001, etc.)
image_mark = f"{identification_prefix}{counter}"

# Image path where the flipped image will be stored
image_path = f"/home/johnbrechbill/whiteboard/{image_mark}.jpg"

# Run libcamera-still with adjusted quality and shutter speed
subprocess.run([
 "libcamera-still",
    "-o", image_path,
    "--quality", "100",             # Set JPEG quality to maximum
    "--exposure", "auto",            # Auto exposure
    "--awb", "auto",                 # Auto white balance
    "--gain", "auto",                # Auto gain
    "--autofocus-mode", "auto",      # Auto focus
    "--drc", "on",                   # Dynamic Range Compression for better contrast
    "--width", "3280",               # Set width based on max resolution
    "--height", "2464",              # Set height based on max resolution
    "-n",                            # No preview window
    "--immediate",                   # Capture immediately
    "--nopreview"
])

# Save the current image path as the last file
with open(last_file_file, 'w') as file:
    file.write(image_path)

# Cloudinary configuration
cloudinary.config(
    cloud_name="db6fegsqa",
    api_key="428688153637693",
    api_secret="nw2mtJx8oAVuxnTQmDxyDQ63we4"
)

# Upload the flipped image with the preset effect
response = cloudinary.uploader.upload(
    image_path,
    public_id=image_mark,
    #upload_preset="PerspectiveAuto"
)

# Get the URL of the transformed image
url, options = cloudinary_url(image_mark)

print("Transformed Image URL:", url)

# Turn on the LED (white)
#pixels[0] = (50, 255, 50)
#time.sleep(.5)  # Keep it on for 1 second

# Turn off the LED
#pixels[0] = (0, 0, 0)
#time.sleep(.5)  # Keep it off for 1 second
