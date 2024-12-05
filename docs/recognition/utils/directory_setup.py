import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def ensure_media_directories(user_id):
    """Create necessary media directories for a user"""
    directories = {
        'datasets': os.path.join(settings.MEDIA_ROOT, 'datasets', f'user_{user_id}'),
        'encodings': os.path.join(settings.MEDIA_ROOT, 'encodings'),
        'face_images': os.path.join(settings.MEDIA_ROOT, 'face_images', f'user_{user_id}'),
        'profile_pics': os.path.join(settings.MEDIA_ROOT, 'profile_pics'),
        'temp': os.path.join(settings.MEDIA_ROOT, 'temp')
    }
    
    try:
        for directory in directories.values():
            os.makedirs(directory, exist_ok=True)
        return directories
    except Exception as e:
        logger.error(f"Error creating directories: {str(e)}")
        return None