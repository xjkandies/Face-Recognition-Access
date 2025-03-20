#!/bin/bash

echo "Setting up Face Recognition Access Control System..."

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads authorized_faces

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download a sample authorized face if none exists
if [ ! -f "authorized_faces/sample_authorized.jpg" ]; then
    echo "Downloading sample authorized face..."
    wget -O authorized_faces/sample_authorized.jpg https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/biden.jpg
fi

# Run the application
echo "Starting the application..."
echo "Once started, open http://localhost:8000 in your web browser"
python3 web_app.py