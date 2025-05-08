import os
import subprocess
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from config import LAST_FILE, CLOUDINARY_CONFIG, UPLOAD_PRESET
from gpio_handler import read_identification

def capture_and_upload_image(counter):
    print("capture and upload image processing...")
    prefix = read_identification()
    image_mark = f"{prefix}{counter}"
    image_path = f"/home/johnbrechbill/whiteboard/{image_mark}.jpg"

    subprocess.run([
        "libcamera-still",
        "-o", image_path,
        "--autofocus-mode", "continuous",
        "--quality", "100",
        "--shutter", "200000",
        "--hdr", "auto",
    ])

    with open(LAST_FILE, 'w') as file:
        file.write(image_path)

    cloudinary.config(**CLOUDINARY_CONFIG)

    response = cloudinary.uploader.upload(
        image_path,
        public_id=image_mark,
        upload_preset=UPLOAD_PRESET
    )

    url, _ = cloudinary_url(image_mark)
    print("Transformed Image URL:", url)

    if os.path.exists(LAST_FILE):
        with open(LAST_FILE, 'r') as file:
            last_image_path = file.read().strip()
        if os.path.exists(last_image_path):
            os.remove(last_image_path)

    return url
