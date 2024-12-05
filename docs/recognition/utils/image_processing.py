import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

def convert_frame_to_rgb(frame_data):
    """Convert frame data to RGB image"""
    try:
        # Convert frame data to numpy array
        nparr = np.frombuffer(frame_data.read(), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            logger.error("Failed to decode frame data")
            return None
            
        # Convert BGR to RGB
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    except Exception as e:
        logger.error(f"Error converting frame to RGB: {str(e)}")
        return None