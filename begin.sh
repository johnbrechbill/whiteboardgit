#!/bin/bash

# Load environment variables (if needed)
source ~/.bashrc

REPO_DIR="/home/johnbrechbill/whiteboardgit"
GIT_URL="https://github.com/johnbrechbill/whiteboardgit.git"
LOG="/home/johnbrechbill/git_repair.log"

echo "[$(date)] Starting begin script" >> $LOG

# Check if .git exists and isn't corrupted
if [ ! -d "$REPO_DIR/.git" ] || ! git -C "$REPO_DIR" status &>/dev/null; then
    echo "[$(date)] Git repo appears corrupted. Re-cloning..." >> $LOG
    rm -rf "$REPO_DIR"
    git clone "$GIT_URL" "$REPO_DIR" >> $LOG 2>&1
    echo "[$(date)] Reclone complete" >> $LOG
else
    echo "[$(date)] Repo healthy. Pulling latest changes..." >> $LOG
    git -C "$REPO_DIR" pull origin main >> $LOG 2>&1
fi

# Run the main script
echo "[$(date)] Starting Python script..." >> $LOG
sudo python3 "$REPO_DIR/onStart.py" >> $LOG 2>&1
