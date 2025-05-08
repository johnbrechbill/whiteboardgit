import board

# NeoPixel
PIXEL_PIN = board.D18
NUM_PIXELS = 9
BRIGHTNESS = 0.8

# GPIO
BUTTON_PIN = 23

# Paths
BLINK_SCRIPT = "/home/johnbrechbill/whiteboardgit/simpleBlink.py"
LAST_FILE = "/home/johnbrechbill/whiteboard/last_file.txt"
COUNTER_FILE = "/home/johnbrechbill/whiteboard/counter.txt"
IDENTIFICATION_FILE = "/home/johnbrechbill/whiteboard/identification.txt"

# Cloudinary
CLOUDINARY_CONFIG = {
    "cloud_name": "db6fegsqa",
    "api_key": "428688153637693",
    "api_secret": "nw2mtJx8oAVuxnTQmDxyDQ63we4"
}
UPLOAD_PRESET = "PerspectiveAuto"
