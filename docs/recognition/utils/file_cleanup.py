import os
import shutil
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def cleanup_temp_files():
    """Clean up temporary files"""
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
        return True
    except Exception as e:
        logger.error(f"Error cleaning temp files: {str(e)}")
        return False

def remove_user_files(user_id):
    """Remove all files associated with a user"""
    try:
        directories = [
            os.path.join(settings.MEDIA_ROOT, 'datasets', f'user_{user_id}'),
            os.path.join(settings.MEDIA_ROOT, 'face_images', f'user_{user_id}'),
            os.path.join(settings.MEDIA_ROOT, 'encodings', f'user_{user_id}_encodings.pickle')
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                if os.path.isdir(directory):
                    shutil.rmtree(directory)
                else:
                    os.remove(directory)
        return True
    except Exception as e:
        logger.error(f"Error removing user files: {str(e)}")
        return False