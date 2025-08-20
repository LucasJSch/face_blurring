import cv2
import numpy as np
import os

class FaceBlurrer:
    def __init__(self):
        # Load the face cascade classifier
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_faces(self, image):
        """Detect faces in an image and return face coordinates"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces
    
    def blur_faces(self, image, blur_strength=51):
        """Apply Gaussian blur to detected faces"""
        faces = self.detect_faces(image)
        result = image.copy()
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_region = result[y:y+h, x:x+w]
            # Apply Gaussian blur
            blurred_face = cv2.GaussianBlur(face_region, (blur_strength, blur_strength), 0)
            # Replace the face region with blurred version
            result[y:y+h, x:x+w] = blurred_face
        
        return result
    
    def pixelate_faces(self, image, pixel_size=20):
        """Apply pixelation effect to detected faces"""
        faces = self.detect_faces(image)
        result = image.copy()
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_region = result[y:y+h, x:x+w]
            
            # Resize down and then up to create pixelation effect
            temp_height, temp_width = face_region.shape[:2]
            small_height = max(1, temp_height // pixel_size)
            small_width = max(1, temp_width // pixel_size)
            
            # Resize down
            small_face = cv2.resize(face_region, (small_width, small_height), interpolation=cv2.INTER_LINEAR)
            # Resize back up
            pixelated_face = cv2.resize(small_face, (temp_width, temp_height), interpolation=cv2.INTER_NEAREST)
            
            # Replace the face region with pixelated version
            result[y:y+h, x:x+w] = pixelated_face
        
        return result
    
    def process_image(self, input_path, output_path, effect='blur'):
        """Process a single image file"""
        image = cv2.imread(input_path)
        if image is None:
            raise ValueError(f"Could not load image from {input_path}")
        
        if effect == 'blur':
            processed = self.blur_faces(image)
        elif effect == 'pixelate':
            processed = self.pixelate_faces(image)
        else:
            raise ValueError(f"Unknown effect: {effect}")
        
        cv2.imwrite(output_path, processed)
        return len(self.detect_faces(image))  # Return number of faces detected
    
    def process_video(self, input_path, output_path, effect='blur'):
        """Process a video file frame by frame"""
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Could not load video from {input_path}")
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        total_faces = 0
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if effect == 'blur':
                processed_frame = self.blur_faces(frame)
            elif effect == 'pixelate':
                processed_frame = self.pixelate_faces(frame)
            else:
                processed_frame = frame
            
            out.write(processed_frame)
            
            # Count faces in every 10th frame to avoid performance issues
            if frame_count % 10 == 0:
                total_faces += len(self.detect_faces(frame))
            
            frame_count += 1
        
        cap.release()
        out.release()
        
        return total_faces