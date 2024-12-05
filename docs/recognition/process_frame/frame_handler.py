import cv2
import numpy as np
import face_recognition
import logging
from ..utils.image_processing import convert_frame_to_rgb
from ..utils.encodings_loader import load_user_encodings

logger = logging.getLogger(__name__)

class FrameHandler:
    def __init__(self, user):
        self.user = user
        self.known_encodings = None
        
    def process(self, frame_data):
        """Process a video frame and return face detection results"""
        try:
            # Load encodings if not already loaded
            if self.known_encodings is None:
                self.known_encodings = load_user_encodings(self.user.id)
                if not self.known_encodings:
                    logger.error(f"Failed to load encodings for user {self.user.id}")
                    return []
            
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
                    name = self.user.username
                
                faces.append({
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top,
                    'name': name,
                    'confidence': round(confidence, 2)
                })
            
            return faces
            
        except Exception as e:
            logger.error(f"Error in frame handler: {str(e)}")
            return []