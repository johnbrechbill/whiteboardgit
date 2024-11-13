#!/bin/bash
source ~/.bashrc
cd /home/johnbrechbill/whiteboardgit
git pull origin main
sudo python3 /home/johnbrechbill/whiteboardgit/onStart.py
