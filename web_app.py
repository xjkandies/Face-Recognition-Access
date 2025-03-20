from flask import Flask, render_template, request, jsonify, send_file
import face_recognition_module as frm
import os
from gtts import gTTS
import base64
import tempfile
import platform
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load authorized faces on startup
authorized_encodings = frm.load_authorized_faces()

def generate_audio(text):
    """Generate audio file and return base64 encoded data."""
    try:
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            # Generate speech with female voice
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file.name)
            
            # Test audio playback based on the operating system
            system = platform.system().lower()
            
            if system == 'windows':
                # For Windows, we'll just return the audio data
                pass
            elif system == 'darwin':
                # For macOS, test with afplay
                subprocess.run(['afplay', temp_file.name], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
            else:
                # For Linux, try different players
                try:
                    # Try mpg321 first
                    subprocess.run(['mpg321', temp_file.name], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
                except FileNotFoundError:
                    try:
                        # Try mpg123 if mpg321 is not available
                        subprocess.run(['mpg123', temp_file.name],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
                    except FileNotFoundError:
                        # Try aplay as last resort
                        subprocess.run(['aplay', temp_file.name],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
            
            # Read the audio file and convert to base64
            with open(temp_file.name, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # Clean up
            os.unlink(temp_file.name)
            
            return audio_data
            
    except Exception as e:
        print(f"Error in speech synthesis: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Verify the face
            is_authorized, message = frm.verify_face(filepath, authorized_encodings)
            
            # Generate audio
            audio_data = generate_audio("Access Granted" if is_authorized else "Access Denied")
            
            # Clean up
            os.unlink(filepath)
            
            return jsonify({
                'success': True,
                'is_authorized': is_authorized,
                'message': message,
                'audio': audio_data
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.unlink(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/preview/<filename>')
def preview_image(filename):
    """Route to preview uploaded images"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            mimetype='image/jpeg'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)