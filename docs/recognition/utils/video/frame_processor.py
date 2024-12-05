import face_recognition
import logging
from ..face_detection import detect_faces
from ..image_processing import convert_frame_to_rgb

logger = logging.getLogger(__name__)

class FrameProcessor:
    def __init__(self):
        self.known_encodings = None
        
    def load_encodings(self, user_id):
        """Load face encodings for the user"""
        from ..encodings_loader import load_user_encodings
        self.known_encodings = load_user_encodings(user_id)
        return self.known_encodings is not None
            
    def process_frame(self, frame_data, username):
        """Process a video frame and return face detection results"""
        try:
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
                face_data = self._process_face(face_encoding, username, top, right, bottom, left)
                if face_data:
                    faces.append(face_data)
            
            return faces
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return []
            
    def _process_face(self, face_encoding, username, top, right, bottom, left):
        """Process a single detected face"""
        try:
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
            
            return {
                'x': left,
                'y': top,
                'width': right - left,
                'height': bottom - top,
                'name': name,
                'confidence': round(confidence, 2)
            }
            
        except Exception as e:
            logger.error(f"Error processing face: {str(e)}")
            return None