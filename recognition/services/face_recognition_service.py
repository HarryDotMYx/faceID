  
from django.conf import settings
import face_recognition
import logging
import numpy as np
from ..utils.image_processing import convert_frame_to_rgb
from ..utils.face_detection import detect_faces
from ..utils.face_matching import match_face

logger = logging.getLogger(__name__)

class FaceRecognitionService:
    def __init__(self):
        self.known_encodings = None
        self.username = None
        
    def initialize(self, user_id, username):
        """Initialize service with user data"""
        self.username = username
        return self.load_encodings(user_id)
        
    def load_encodings(self, user_id):
        """Load face encodings for the user"""
        from ..utils.encodings_loader import load_user_encodings
        self.known_encodings = load_user_encodings(user_id)
        return self.known_encodings is not None
            
    def process_frame(self, frame_data):
        """Process a video frame and return face detection results"""
        try:
            # Convert frame to RGB
            rgb_frame = convert_frame_to_rgb(frame_data)
            if rgb_frame is None:
                return []
                
            # Detect faces
            face_locations, face_encodings = detect_faces(rgb_frame)
            if not face_locations:
                return []
            
            # Process detected faces
            faces = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                name, confidence = match_face(
                    face_encoding, 
                    self.known_encodings,
                    self.username
                )
                
                faces.append({
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top,
                    'name': name,
                    'confidence': confidence
                })
            
            return faces
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return []
  