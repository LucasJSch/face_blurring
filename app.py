import os
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename
from face_blur import FaceBlurrer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS

# Initialize face blurrer with default settings (will be reconfigured per request)
face_blurrer = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def is_video_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    effect = request.form.get('effect', 'blur')
    model_type = request.form.get('model_type', 'haar_default')
    blur_strength = request.form.get('blur_strength', '51')
    pixel_size = request.form.get('pixel_size', '20')
    
    # Convert parameters to appropriate types
    try:
        blur_strength = int(blur_strength)
        pixel_size = int(pixel_size)
    except ValueError:
        return jsonify({'error': 'Invalid parameter values'}), 400
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Initialize face blurrer with specified parameters
        face_blurrer = FaceBlurrer(model_type=model_type, blur_strength=blur_strength, pixel_size=pixel_size)
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(upload_path)
        
        # Process the file
        processed_filename = f"processed_{unique_filename}"
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
        
        if is_image_file(original_filename):
            faces_detected = face_blurrer.process_image(upload_path, processed_path, effect, blur_strength, pixel_size)
            file_type = 'image'
        elif is_video_file(original_filename):
            faces_detected = face_blurrer.process_video(upload_path, processed_path, effect, blur_strength, pixel_size)
            file_type = 'video'
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        return jsonify({
            'success': True,
            'original_filename': original_filename,
            'original_url': url_for('uploaded_file', filename=unique_filename),
            'processed_url': url_for('processed_file', filename=processed_filename),
            'faces_detected': faces_detected,
            'file_type': file_type,
            'effect': effect,
            'model_type': model_type,
            'blur_strength': blur_strength,
            'pixel_size': pixel_size
        })
        
    except Exception as e:
        # Clean up files if processing failed
        if 'upload_path' in locals() and os.path.exists(upload_path):
            os.remove(upload_path)
        if 'processed_path' in locals() and os.path.exists(processed_path):
            os.remove(processed_path)
        
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    # Ensure upload and processed directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=True)