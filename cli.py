import os
import face_recognition_module as frm
from config import AUTHORIZED_FACES_DIR

def main():
    print("\nFace Recognition Access Control System (CLI Version)")
    print("=" * 50)
    
    # Load authorized faces
    print("\nLoading authorized faces...")
    authorized_encodings = frm.load_authorized_faces()
    print(f"Number of authorized faces loaded: {len(authorized_encodings)}")
    
    while True:
        print("\nOptions:")
        print("1. Verify a face image")
        print("2. List authorized faces")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            image_path = input("\nEnter the path to the image file: ")
            if not os.path.exists(image_path):
                print("Error: File does not exist!")
                continue
                
            print("\nVerifying face...")
            is_authorized, message = frm.verify_face(image_path, authorized_encodings)
            
            if is_authorized:
                print("\n✅ " + message)
            else:
                print("\n❌ " + message)
                
        elif choice == "2":
            print("\nAuthorized Faces:")
            if os.path.exists(AUTHORIZED_FACES_DIR):
                files = os.listdir(AUTHORIZED_FACES_DIR)
                if files:
                    for i, file in enumerate(files, 1):
                        if frm.is_allowed_file(file):
                            print(f"{i}. {file}")
                else:
                    print("No authorized faces found.")
            else:
                print("Authorized faces directory not found.")
                
        elif choice == "3":
            print("\nThank you for using Face Recognition Access Control System!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()