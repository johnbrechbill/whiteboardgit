#!/bin/bash

# Load user environment
source ~/.bashrc

# Set repo directory
REPO_DIR="/home/johnbrechbill/whiteboardgit"
REPO_URL="https://github.com/johnbrechbill/whiteboardgit.git"

# Function to reset repo if corrupted
reset_repo() {
    echo "Resetting corrupted repository..."
    rm -rf "$REPO_DIR"
    git clone "$REPO_URL" "$REPO_DIR"
}

# Navigate to repo
cd "$REPO_DIR" || { echo "Repo dir missing. Cloning fresh..."; git clone "$REPO_URL" "$REPO_DIR"; cd "$REPO_DIR"; }

# Check for corruption
if ! git fsck --full > /dev/null 2>&1; then
    echo "Git repo is corrupted. Attempting recovery..."
    reset_repo
else
    echo "Git repo is healthy. Pulling latest..."
    git fetch origin
    git reset --hard origin/main  # Ensure clean sync with origin
fi

# Run script
sudo python3 "$REPO_DIR/onStart.py"
