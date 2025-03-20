import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import face_recognition_module as frm
from gtts import gTTS
import tempfile
import subprocess
from config import (
    WINDOW_SIZE, WINDOW_TITLE, THEME,
    SUCCESS_COLOR, ERROR_COLOR, PRIMARY_COLOR,
    HEADER_FONT, NORMAL_FONT, BUTTON_FONT
)

class FaceRecognitionApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Apply theme
        style = ttk.Style()
        style.theme_use(THEME)
        
        # Configure custom styles
        style.configure('Success.TLabel', foreground=SUCCESS_COLOR, font=NORMAL_FONT)
        style.configure('Error.TLabel', foreground=ERROR_COLOR, font=NORMAL_FONT)
        style.configure('Header.TLabel', font=HEADER_FONT, foreground=PRIMARY_COLOR)
        style.configure('Custom.TButton', 
                       font=BUTTON_FONT, 
                       background=PRIMARY_COLOR,
                       foreground='white')
        style.configure('Primary.TFrame', background=PRIMARY_COLOR)

        # Load authorized faces
        self.authorized_encodings = frm.load_authorized_faces()
        
        # Initialize variables
        self.current_image_path = None
        self.photo = None  # Keep reference to prevent garbage collection
        
        self.setup_ui()

    def speak_message(self, text):
        """Convert text to speech and play it."""
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                # Generate speech with female voice
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_file.name)
                
                # Play the audio using mpg321
                subprocess.run(['mpg321', temp_file.name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Clean up the temporary file
                os.unlink(temp_file.name)
        except Exception as e:
            print(f"Error in speech synthesis: {str(e)}")

    def setup_ui(self):
        """Set up the user interface."""
        # Main container with primary color header
        header_frame = ttk.Frame(self.root, style='Primary.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew')
        self.root.grid_columnconfigure(0, weight=1)
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=1, column=0, sticky='nsew')
        
        # Header with primary color background
        header_label = ttk.Label(
            header_frame, 
            text="Face Recognition Access Control",
            style='Header.TLabel',
            padding="10"
        )
        header_label.grid(row=0, column=0, pady=(10, 10))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Image preview frame with primary color border
        self.preview_frame = ttk.LabelFrame(
            main_frame,
            text="Image Preview",
            padding="10",
            style='Custom.TButton'
        )
        self.preview_frame.grid(row=1, column=0, columnspan=2, pady=(20, 20), sticky='nsew')
        
        # Preview label
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.grid(row=0, column=0, padx=5, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
        
        # Upload button with primary color
        self.upload_btn = ttk.Button(
            button_frame,
            text="Upload Image",
            style='Custom.TButton',
            command=self.upload_image
        )
        self.upload_btn.grid(row=0, column=0, padx=5)
        
        # Verify button with primary color
        self.verify_btn = ttk.Button(
            button_frame,
            text="Verify Face",
            style='Custom.TButton',
            command=self.verify_face,
            state='disabled'
        )
        self.verify_btn.grid(row=0, column=1, padx=5)
        
        # Clear button with primary color
        self.clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            style='Custom.TButton',
            command=self.clear_preview,
            state='disabled'
        )
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Result label
        self.result_label = ttk.Label(
            main_frame,
            text="",
            font=NORMAL_FONT
        )
        self.result_label.grid(row=3, column=0, columnspan=2, pady=(0, 20))
        
        # Status label with primary color
        self.status_label = ttk.Label(
            main_frame,
            text=f"Authorized faces loaded: {len(self.authorized_encodings)}",
            font=NORMAL_FONT,
            foreground=PRIMARY_COLOR
        )
        self.status_label.grid(row=4, column=0, columnspan=2)

        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def upload_image(self):
        """Handle image upload."""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="Select an image",
            filetypes=file_types
        )
        
        if filename:
            try:
                # Open and resize image for preview
                image = Image.open(filename)
                image.thumbnail((400, 400))  # Resize for preview
                self.photo = ImageTk.PhotoImage(image)
                
                # Update preview
                self.preview_label.configure(image=self.photo)
                
                # Store image path and update button states
                self.current_image_path = filename
                self.verify_btn.configure(state='normal')
                self.clear_btn.configure(state='normal')
                
                # Clear previous result
                self.result_label.configure(text="")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def verify_face(self):
        """Verify the uploaded face against authorized faces."""
        if not self.current_image_path:
            messagebox.showwarning("Warning", "Please upload an image first")
            return
            
        # Verify face
        is_authorized, message = frm.verify_face(
            self.current_image_path,
            self.authorized_encodings
        )
        
        # Update result label and speak the result
        if is_authorized:
            self.result_label.configure(
                text=message,
                foreground=SUCCESS_COLOR
            )
            self.speak_message("Access Granted")
        else:
            self.result_label.configure(
                text=message,
                foreground=ERROR_COLOR
            )
            self.speak_message("Access Denied")

    def clear_preview(self):
        """Clear the image preview and reset the UI."""
        self.preview_label.configure(image='')
        self.current_image_path = None
        self.photo = None
        self.verify_btn.configure(state='disabled')
        self.clear_btn.configure(state='disabled')
        self.result_label.configure(text="")

    def run(self):
        """Start the application."""
        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Start main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.run()