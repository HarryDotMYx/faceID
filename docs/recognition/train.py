import os
import cv2
import face_recognition
import pickle
import logging
from django.conf import settings
from pathlib import Path
from imutils import paths
import numpy as np
from .utils.dataset_manager import DatasetManager

logger = logging.getLogger(__name__)

def train_user_model(user_id):
    """Train the face recognition model for a specific user"""
    try:
        # Initialize dataset manager
        dataset_manager = DatasetManager(user_id)
        
        # Get dataset images
        dataset_images = dataset_manager.get_dataset_images()
        if not dataset_images:
            return False, "No face images found. Please upload some images first."
        
        logger.info(f"[INFO] Processing {len(dataset_images)} images for user {user_id}")
        
        # Initialize lists for encodings and names
        known_encodings = []
        known_names = []
        
        # Process each image
        for image_name in dataset_images:
            try:
                image_path = os.path.join(dataset_manager.dataset_path, image_name)
                
                # Load and convert image
                image = cv2.imread(image_path)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Detect faces and compute encodings
                boxes = face_recognition.face_locations(rgb, model="hog")
                
                if not boxes:
                    logger.warning(f"No face detected in {image_path}")
                    continue
                
                # Compute face encodings
                encodings = face_recognition.face_encodings(rgb, boxes)
                
                # Store encodings
                for encoding in encodings:
                    known_encodings.append(encoding)
                    known_names.append(str(user_id))
                    
            except Exception as e:
                logger.error(f"Error processing {image_path}: {str(e)}")
                continue
        
        if not known_encodings:
            return False, "Could not encode any faces from the uploaded images."
        
        # Save encodings
        logger.info("[INFO] Serializing encodings...")
        data = {
            "encodings": known_encodings,
            "names": known_names
        }
        
        encoding_path = os.path.join(dataset_manager.encoding_path, f'user_{user_id}_encodings.pickle')
        
        with open(encoding_path, "wb") as f:
            f.write(pickle.dumps(data))
        
        return True, f"Successfully encoded {len(known_encodings)} faces"
        
    except Exception as e:
        logger.error(f"Error during training: {str(e)}")
        return False, f"Training failed: {str(e)}"