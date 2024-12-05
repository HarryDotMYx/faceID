import os
import logging
from django.conf import settings

def ensure_user_directories(user_id):
    """Create necessary directories for user data"""
    directories = {
        'dataset': os.path.join(settings.MEDIA_ROOT, f'face_images/user_{user_id}'),
        'encoding': os.path.join(settings.MEDIA_ROOT, 'encodings'),
        'profile': os.path.join(settings.MEDIA_ROOT, 'profile_pics'),
        'temp': os.path.join(settings.MEDIA_ROOT, 'temp')
    }
    
    for directory in directories.values():
        os.makedirs(directory, exist_ok=True)
    
    return directories

def get_user_paths(user_id):
    """Get all relevant paths for a user"""
    return {
        'dataset': os.path.join(settings.MEDIA_ROOT, f'face_images/user_{user_id}'),
        'encoding': os.path.join(settings.MEDIA_ROOT, f'encodings/user_{user_id}_encodings.pickle'),
        'latest_image': os.path.join(settings.MEDIA_ROOT, f'face_images/user_{user_id}/latest.jpg')
    }

def cleanup_temp_files():
    """Clean up temporary files"""
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    try:
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
    except Exception as e:
        logging.error(f"Error cleaning temp files: {str(e)}")