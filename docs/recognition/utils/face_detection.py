import face_recognition
import logging

logger = logging.getLogger(__name__)

def detect_faces(rgb_frame):
    """Detect faces in an RGB frame"""
    try:
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        if not face_locations:
            return [], []
            
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        return face_locations, face_encodings
        
    except Exception as e:
        logger.error(f"Error detecting faces: {str(e)}")
        return [], []