import face_recognition
import logging

logger = logging.getLogger(__name__)

def match_face(face_encoding, known_encodings, username, tolerance=0.6):
    """Match a face encoding against known encodings"""
    try:
        if not known_encodings:
            return "Unknown", 0
            
        matches = face_recognition.compare_faces(
            known_encodings,
            face_encoding,
            tolerance=tolerance
        )
        
        if True in matches:
            confidence = (matches.count(True) / len(matches)) * 100
            return username, round(confidence, 2)
            
        return "Unknown", 0
        
    except Exception as e:
        logger.error(f"Error matching face: {str(e)}")
        return "Unknown", 0