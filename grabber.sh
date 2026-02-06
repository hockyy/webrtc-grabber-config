#!/bin/bash

SEAT_NUMBER=001  # Change me
HOST_IP=10.119.84.35

# Ensure v4l-utils is installed
if ! dpkg -s v4l-utils &>/dev/null; then
    echo "v4l-utils not found. Installing..."
    sudo apt update && sudo apt install -y v4l-utils
fi
echo "v4l-utils is installed."

# Setup directory
mkdir -p ~/core
cd ~/core

# Download and extract if not already done
if [ ! -d "webrtc_grabber_linux_x64" ]; then
    echo "Downloading webrtc grabber..."
    wget -c https://github.com/irdkwmnsb/webrtc-grabber/releases/download/v1.1.0/webrtc_grabber_agent_linux_x64.tar.gz.zip

    echo "Unzipping..."
    unzip webrtc_grabber_agent_linux_x64.tar.gz.zip

    echo "Extracting tar.gz..."
    tar -xzf webrtc_grabber_agent_linux_x64.tar.gz

    # Cleanup archives
    rm -f webrtc_grabber_agent_linux_x64.tar.gz.zip webrtc_grabber_agent_linux_x64.tar.gz
fi

# Write config.json
cat > ~/core/webrtc_grabber_linux_x64/config.json << 'EOF'
{
  "webcamConstraint": {
    "aspectRatio": 1.7777777778
  },
  "webcamAudioConstraint": true,
  "desktopConstraint": {
    "width": 1280,
    "height": 720
  }
}
EOF
echo "config.json written."

# Run grabber
cd ~/core/webrtc_grabber_linux_x64
bash grabber-linux.sh run ${SEAT_NUMBER} ws://${HOST_IP}:13478
