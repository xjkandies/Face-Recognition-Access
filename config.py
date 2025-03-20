import os

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory for storing authorized face images
AUTHORIZED_FACES_DIR = os.path.join(BASE_DIR, "authorized_faces")

# Create authorized_faces directory if it doesn't exist
if not os.path.exists(AUTHORIZED_FACES_DIR):
    os.makedirs(AUTHORIZED_FACES_DIR)

# Allowed image file extensions
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# Face recognition tolerance (lower is more strict)
FACE_MATCH_TOLERANCE = 0.6

# UI Configuration
WINDOW_SIZE = "800x600"
WINDOW_TITLE = "Face Recognition Access Control"
THEME = "clam"  # Modern ttk theme

# Colors
SUCCESS_COLOR = "#28a745"  # Green
ERROR_COLOR = "#dc3545"    # Red
PRIMARY_COLOR = "#007bff"  # Blue

# Font configurations
HEADER_FONT = ("Helvetica", 24, "bold")
NORMAL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 12, "bold")