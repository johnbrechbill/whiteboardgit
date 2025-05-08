#!/usr/bin/env python3

import sys
from ssh_setup import setup_ssh_agent
from button_listener import setup_gpio, wait_for_button
from config import TEST_SCRIPT

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/home/johnbrechbill/whiteboard/lib/python3.11/site-packages')

setup_ssh_agent()
setup_gpio()
wait_for_button(TEST_SCRIPT)
