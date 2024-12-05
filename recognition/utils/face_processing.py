import cv2
import face_recognition
import numpy as np
from PIL import Image, ExifTags
from .dataset_manager import DatasetManager
import os
import logging
import shutil

logger = logging.getLogger(__name__)

def process_uploaded_face(image_path, user_id):
    """Process and validate uploaded face image"""
    try:
        # Initialize dataset manager
        dataset_manager = DatasetManager(user_id)
        
        # Preprocess the image
        image = preprocess_image(image_path)
        if image is None:
            return False, "Failed to process the image. Please try another image."
        
        # Try face detection
        face_locations = face_recognition.face_locations(image, model="hog")
        
        if not face_locations:
            # Try with different parameters
            face_locations = face_recognition.face_locations(image, model="hog", number_of_times_to_upsample=2)
            
        if not face_locations:
            return False, "No face detected in the image. Please ensure your face is clearly visible."
            
        if len(face_locations) > 1:
            return False, "Multiple faces detected. Please upload an image with only your face."
        
        # Add image to dataset
        image_name = os.path.basename(image_path)
        success, message = dataset_manager.add_image(image_path, image_name)
        
        if not success:
            return False, f"Failed to add image to dataset: {message}"
        
        return True, "Face processed successfully"
        
    except Exception as e:
        logger.error(f"Error processing face image: {str(e)}")
        return False, f"Error processing image: {str(e)}"

def preprocess_image(image_path):
    """Preprocess image to improve face detection"""
    try:
        # Read image using PIL first to handle orientation
        pil_image = Image.open(image_path)
        
        # Convert to RGB mode if necessary
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Handle EXIF orientation
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(pil_image._getexif().items())
            
            if exif[orientation] == 3:
                pil_image = pil_image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                pil_image = pil_image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                pil_image = pil_image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # No EXIF data or no orientation tag
            pass
        
        # Convert to numpy array
        image = np.array(pil_image)
        
        return image
        
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None