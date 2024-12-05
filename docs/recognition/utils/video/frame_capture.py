import cv2
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class FrameCapture:
    @staticmethod
    def capture_frame(video_element, width=640, height=480):
        """Capture frame from video element and convert to proper format"""
        try:
            canvas = document.createElement('canvas')
            canvas.width = width
            canvas.height = height
            ctx = canvas.getContext('2d')
            ctx.drawImage(video_element, 0, 0)
            
            return canvas.toBlob(resolve => {
                resolve(blob)
            }, 'image/jpeg', 0.8)
        except Exception as e:
            logger.error(f"Error capturing frame: {str(e)}")
            return None