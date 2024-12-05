import os
import shutil
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class DatasetManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.dataset_path = os.path.join(settings.MEDIA_ROOT, 'datasets', f'user_{user_id}')
        self.encoding_path = os.path.join(settings.MEDIA_ROOT, 'encodings')
        
    def setup_directories(self):
        """Create necessary directories for the dataset"""
        try:
            os.makedirs(self.dataset_path, exist_ok=True)
            os.makedirs(self.encoding_path, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directories: {str(e)}")
            return False
            
    def add_image(self, image_path, image_name):
        """Add an image to the user's dataset"""
        try:
            if not os.path.exists(image_path):
                return False, "Source image does not exist"
                
            # Ensure directories exist
            self.setup_directories()
            
            # Copy image to dataset
            dest_path = os.path.join(self.dataset_path, image_name)
            shutil.copy2(image_path, dest_path)
            
            return True, "Image added to dataset successfully"
        except Exception as e:
            logger.error(f"Error adding image to dataset: {str(e)}")
            return False, str(e)
            
    def remove_image(self, image_name):
        """Remove an image from the dataset"""
        try:
            image_path = os.path.join(self.dataset_path, image_name)
            if os.path.exists(image_path):
                os.remove(image_path)
                return True, "Image removed successfully"
            return False, "Image not found in dataset"
        except Exception as e:
            logger.error(f"Error removing image from dataset: {str(e)}")
            return False, str(e)
            
    def get_dataset_images(self):
        """Get list of images in the dataset"""
        try:
            if not os.path.exists(self.dataset_path):
                return []
            return [f for f in os.listdir(self.dataset_path) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        except Exception as e:
            logger.error(f"Error getting dataset images: {str(e)}")
            return []
            
    def clear_dataset(self):
        """Remove all images from the dataset"""
        try:
            if os.path.exists(self.dataset_path):
                shutil.rmtree(self.dataset_path)
            self.setup_directories()
            return True, "Dataset cleared successfully"
        except Exception as e:
            logger.error(f"Error clearing dataset: {str(e)}")
            return False, str(e)