  
import logging
from .face_recognition_service import FaceRecognitionService
from ..utils.fps_calculator import FPSCalculator

logger = logging.getLogger(__name__)

class FrameProcessingService:
    def __init__(self):
        self.face_recognition = FaceRecognitionService()
        self.fps_calculator = FPSCalculator()
        
    def initialize(self, user_id, username):
        """Initialize services"""
        return self.face_recognition.initialize(user_id, username)
        
    def process_frame(self, frame_data):
        """Process a single frame"""
        try:
            # Update FPS
            self.fps_calculator.update()
            
            # Process frame for face detection
            faces = self.face_recognition.process_frame(frame_data)
            
            # Add FPS to response
            if faces:
                faces[0]['fps'] = self.fps_calculator.get_fps()
                
            return faces
            
        except Exception as e:
            logger.error(f"Error in frame processing: {str(e)}")
            return []
  