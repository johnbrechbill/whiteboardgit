import sys
import os

sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

from picamera2 import Picamera2
import time
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

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

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for still capture
camera_config = picam2.create_still_configuration(main={"size": (3280, 2464)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)

# Start the camera
picam2.start()

# Wait for the camera to adjust
time.sleep(2)

# Capture the image
image_path = f"/home/johnbrechbill/whiteboard/{image_mark}.jpg"
picam2.capture_file(image_path)

# Save the current image path as the last file
with open(last_file_file, 'w') as file:
    file.write(image_path)

# Stop the camera
picam2.stop()

# Cloudinary configuration
cloudinary.config(
    cloud_name="db6fegsqa",
    api_key="428688153637693",
    api_secret="nw2mtJx8oAVuxnTQmDxyDQ63we4"
)
# Upload the image with the distort effect
response = cloudinary.uploader.upload(
    image_path,
    public_id=image_mark,
    upload_preset="PerspectiveAuto", "deArc"
   
)

# Get the URL of the transformed image
url, options = cloudinary_url(image_mark)

print("Transformed Image URL:", url)
print("github updated this code yayyyyy")
