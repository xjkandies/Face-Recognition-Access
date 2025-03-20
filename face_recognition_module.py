import os
import face_recognition
import numpy as np
from PIL import Image

def load_authorized_faces():
    """Load and encode all authorized faces from the authorized_faces directory."""
    authorized_encodings = []
    authorized_dir = "authorized_faces"
    
    if not os.path.exists(authorized_dir):
        os.makedirs(authorized_dir)
        return authorized_encodings
    
    for filename in os.listdir(authorized_dir):
        if is_allowed_file(filename):
            image_path = os.path.join(authorized_dir, filename)
            try:
                # Load and validate image using PIL
                with Image.open(image_path) as img:
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # Validate image dimensions
                    if img.size[0] < 50 or img.size[1] < 50:
                        print(f"Warning: Image {filename} is too small for reliable face detection")
                        continue
                    # Save as RGB if needed
                    if img.mode != 'RGB':
                        rgb_path = image_path + '_rgb.jpg'
                        img.save(rgb_path)
                        image_path = rgb_path

                # Load the image and get face encodings
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    # Add the first face encoding found in the image
                    authorized_encodings.append(encodings[0])
                else:
                    print(f"Warning: No face detected in {filename}")
                    
                # Clean up temporary RGB file if created
                if image_path.endswith('_rgb.jpg'):
                    os.remove(image_path)
                    
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    return authorized_encodings

def verify_face(image_path, authorized_encodings):
    """Verify if the face in the image matches any authorized face."""
    try:
        # Validate and preprocess image using PIL
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
                # Save as temporary RGB file
                rgb_path = image_path + '_rgb.jpg'
                img.save(rgb_path)
                image_path = rgb_path

            # Check image quality
            if img.size[0] < 50 or img.size[1] < 50:
                return False, "Image resolution is too low for reliable face detection"

        # Load and encode the face to verify
        image_to_verify = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image_to_verify)
        
        # Clean up temporary RGB file if created
        if image_path.endswith('_rgb.jpg'):
            os.remove(image_path)
        
        if not face_locations:
            return False, "No face detected in the image"
        
        if len(face_locations) > 1:
            return False, "Multiple faces detected. Please upload an image with a single face"
        
        face_encoding = face_recognition.face_encodings(image_to_verify, face_locations)[0]
        
        # Check if the face matches any authorized face
        if not authorized_encodings:
            return False, "No authorized faces in the database"
        
        # Calculate face distances
        face_distances = face_recognition.face_distance(authorized_encodings, face_encoding)
        matches = face_recognition.compare_faces(authorized_encodings, face_encoding)
        
        if True in matches:
            best_match_index = np.argmin(face_distances)
            confidence = 1 - face_distances[best_match_index]
            return True, f"Access Granted (Confidence: {confidence:.2%})"
        else:
            closest_distance = min(face_distances)
            return False, f"Access Denied (Best match distance: {closest_distance:.2f})"
            
    except Exception as e:
        return False, f"Error during face verification: {str(e)}"

def is_allowed_file(filename):
    """Check if the file has an allowed extension."""
    allowed_extensions = {'.jpg', '.jpeg', '.png'}
    return os.path.splitext(filename.lower())[1] in allowed_extensions