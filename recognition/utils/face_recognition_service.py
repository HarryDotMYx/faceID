  
import cv2
import face_recognition
import numpy as np
import logging
import time
from datetime import datetime
from .file_handlers import get_user_paths
import pickle

logger = logging.getLogger(__name__)

class FaceRecognitionService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.frame_count = 0
        self.fps_start_time = None
        self.fps = 0
        
    def load_known_faces(self, user_id):
        """Load known face encodings for the user"""
        try:
            user_paths = get_user_paths(user_id)
            with open(user_paths['encoding'], 'rb') as f:
                data = pickle.loads(f.read())
                self.known_face_encodings = data["encodings"]
                self.known_face_names = data["names"]
            return True
        except Exception as e:
            logger.error(f"Error loading known faces: {str(e)}")
            return False
            
    def process_frame(self, frame_data, user_id):
        """Process a video frame and return face detection results"""
        try:
            # Update FPS calculation
            if self.frame_count == 0:
                self.fps_start_time = time.time()
            self.frame_count += 1
            
            if self.frame_count >= 30:  # Calculate FPS every 30 frames
                self.fps = self.frame_count / (time.time() - self.fps_start_time)
                self.frame_count = 0
            
            # Convert frame data to numpy array
            nparr = np.frombuffer(frame_data.read(), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces in the frame
            face_locations = face_recognition.face_locations(
                rgb_frame,
                model="hog",
                number_of_times_to_upsample=1
            )
            
            if not face_locations:
                return []
                
            # Get face encodings
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            # Process each detected face
            faces = []
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding,
                    tolerance=0.6
                )
                
                name = "Unknown"
                confidence = 0
                
                if True in matches:
                    matched_idxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}
                    
                    # Calculate confidence based on number of matches
                    for i in matched_idxs:
                        name = self.known_face_names[i]
                        counts[name] = counts.get(name, 0) + 1
                    
                    name = max(counts, key=counts.get)
                    confidence = (counts[name] / len(matched_idxs)) * 100
                
                faces.append({
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top,
                    'name': name,
                    'confidence': round(confidence, 2),
                    'timestamp': datetime.now().isoformat(),
                    'fps': round(self.fps, 1)
                })
                
                # Log detection event
                logger.info(
                    f"[{datetime.now()}] Face detected - "
                    f"Name: {name}, Confidence: {confidence:.2f}%, "
                    f"FPS: {self.fps:.1f}"
                )
            
            return faces
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return []
  