# Face Recognition Access Control System

A web-based face recognition system with voice feedback that verifies faces against an authorized database.

## Prerequisites

Before running the system, make sure you have Python 3.10+ installed on your computer.

## Installation Steps

1. First, navigate to the project directory:
```bash
cd face_recognition_app
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create necessary directories:
```bash
mkdir -p uploads authorized_faces
```

4. Add at least one authorized face:
   - Place a photo of an authorized person in the `authorized_faces` directory
   - Name it something like `authorized1.jpg`
   - Supported formats: JPG, JPEG, PNG

## Running the Application

1. Start the web application:
```bash
python3 web_app.py
```

2. Open your web browser and go to:
```
http://localhost:8000
```

## Using the System

The web interface offers three ways to test face recognition:

1. **Quick Test Buttons:**
   - Click "Test Authorized Face" to verify an authorized face
   - Click "Test Unauthorized Face" to test with an unauthorized face

2. **Upload Your Own Image:**
   - Drag and drop an image onto the upload area
   - Or click the upload area to select a file
   - Click "Verify Face" to check the image

3. **Results:**
   - The system will display "Access Granted" or "Access Denied"
   - A female voice will announce the result
   - Visual feedback shows green for granted access and red for denied access

## Troubleshooting

1. If you get a "port already in use" error:
   - Kill the existing process: `pkill -f "python3 web_app.py"`
   - Try running the application again

2. If dependencies fail to install:
   - Try installing them one by one from requirements.txt
   - Make sure you have Python development headers installed:
     ```bash
     # On Ubuntu/Debian:
     sudo apt-get install python3-dev
     
     # On CentOS/RHEL:
     sudo yum install python3-devel
     ```

3. If face recognition is not working:
   - Make sure the image is clear and well-lit
   - Verify that the face is clearly visible in the image
   - Check that the authorized_faces directory contains at least one reference image

## System Requirements

- Python 3.10 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Microphone enabled for voice feedback
- Webcam (optional, for live capture)

## Features

- Face Recognition with dlib
- Female voice feedback using Google Text-to-Speech
- Modern UI with Tailwind CSS
- Drag-and-drop file upload
- Real-time visual feedback
- Support for multiple image formats