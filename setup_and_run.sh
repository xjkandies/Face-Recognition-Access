#!/bin/bash

echo "Setting up Face Recognition Access Control System..."

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads authorized_faces

# Detect OS
OS="$(uname -s)"

# Install system dependencies based on OS
echo "Installing system dependencies..."
case "${OS}" in
    Linux*)
        if [ -f /etc/debian_version ]; then
            # Debian/Ubuntu
            sudo apt-get update
            sudo apt-get install -y python3-pip mpg321 mpg123 alsa-utils
        elif [ -f /etc/redhat-release ]; then
            # CentOS/RHEL
            sudo yum install -y python3-pip mpg123
        elif [ -f /etc/arch-release ]; then
            # Arch Linux
            sudo pacman -Sy python-pip mpg123
        fi
        ;;
    Darwin*)
        # macOS
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3
        ;;
    MINGW*|CYGWIN*|MSYS*)
        # Windows
        echo "Windows detected. Make sure you have Python installed."
        ;;
    *)
        echo "Unknown operating system"
        ;;
esac

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download a sample authorized face if none exists
if [ ! -f "authorized_faces/sample_authorized.jpg" ]; then
    echo "Downloading sample authorized face..."
    wget -O authorized_faces/sample_authorized.jpg https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/biden.jpg
fi

# Test audio playback
echo "Testing audio playback..."
python3 - << EOF
from gtts import gTTS
import tempfile
import os
import platform
import subprocess

def test_audio():
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            tts = gTTS(text="Audio test successful", lang='en', slow=False)
            tts.save(temp_file.name)
            
            system = platform.system().lower()
            if system == 'windows':
                from playsound import playsound
                playsound(temp_file.name)
            elif system == 'darwin':
                subprocess.run(['afplay', temp_file.name])
            else:
                try:
                    subprocess.run(['mpg321', temp_file.name])
                except FileNotFoundError:
                    try:
                        subprocess.run(['mpg123', temp_file.name])
                    except FileNotFoundError:
                        subprocess.run(['aplay', temp_file.name])
            
            os.unlink(temp_file.name)
            print("Audio test successful!")
    except Exception as e:
        print(f"Audio test failed: {str(e)}")
        print("Please install appropriate audio playback software for your system")

test_audio()
EOF

# Run the application
echo "Starting the application..."
echo "Once started, open http://localhost:8000 in your web browser"
python3 web_app.py