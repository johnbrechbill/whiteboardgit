import sys
sys.path.append('/usr/lib/python3/dist-packages')  # Add system-wide packages path
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

from picamera2 import Picamera2
import time
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# Initialize the camera
picam2 = Picamera2()

# Configure the camera for still capture
camera_config = picam2.create_still_configuration(main={"size": (640, 480)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)

# Start the camera
picam2.start()

# Wait for the camera to adjust
time.sleep(2)

# Capture the image
image_path = "/home/johnbrechbill/whiteboard/test.jpg"
picam2.capture_file(image_path)

# Stop the camera
picam2.stop()

# Configure Cloudinary
cloudinary.config( 
    cloud_name = "db6fegsqa", 
    api_key = "428688153637693", 
    api_secret = "nw2mtJx8oAVuxnTQmDxyDQ63we4", 
    secure=True
)

# Upload the image to Cloudinary
response = cloudinary.uploader.upload(image_path)
public_id = response['public_id']

# Apply the e_distort effect with specific coordinates
transformed_image_url, options = cloudinary_url(
    public_id,
    transformation=[
        {
            "effect": "distort:40:25:280:60:260:155:35:165",  # Apply perspective transformation with specific coordinates
            "crop": "fit",
            "width": 500,
            "height": 500
        }
    ]
)

# Print the URLs
print(f"Image uploaded to Cloudinary. URL: {response['secure_url']}")
print(f"Transformed image URL (with perspective distortion): {transformed_image_url}")
print("github updated!!")
