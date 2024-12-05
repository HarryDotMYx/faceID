import cv2
import numpy as np
import face_recognition
import logging
from .face_detection import detect_faces
from .face_matching import match_face
from .image_processing import convert_frame_to_rgb
from .fps_calculator import FPSCalculator
from .encodings_loader import load_user_encodings

logger = logging.getLogger(__name__)

class FrameProcessor:
    def __init__(self):
        self.known_encodings = None
        self.fps_calculator = FPSCalculator()
        
    def load_encodings(self, user_id):
        """Load face encodings for the user"""
        self.known_encodings = load_user_encodings(user_id)
        return self.known_encodings is not None
            
    def process_frame(self, frame_data, user_id, username):
        """Process a video frame and return face detection results"""
        try:
            # Update FPS
            self.fps_calculator.update()
            
            # Convert frame to RGB
            rgb_frame = convert_frame_to_rgb(frame_data)
            if rgb_frame is None:
                return []
                
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            if not face_locations:
                return []
                
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            # Process detected faces
            faces = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(
                    self.known_encodings,
                    face_encoding,
                    tolerance=0.6
                )
                
                name = "Unknown"
                confidence = 0
                
                if True in matches:
                    confidence = (matches.count(True) / len(matches)) * 100
                    name = username
                
                faces.append({
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top,
                    'name': name,
                    'confidence': round(confidence, 2),
                    'fps': self.fps_calculator.get_fps()
                })
            
            return faces
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return []