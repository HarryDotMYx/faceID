from django.core.exceptions import ValidationError
import magic
import logging

logger = logging.getLogger(__name__)

def validate_upload(file):
    """Validate uploaded file"""
    try:
        # Check file size (max 5MB)
        if file.size > 5 * 1024 * 1024:
            return False, 'File size must not exceed 5MB'
            
        # Check MIME type
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)
        
        if mime not in ['image/jpeg', 'image/png']:
            return False, 'Invalid file type. Please upload a JPEG or PNG image'
            
        return True, None
        
    except Exception as e:
        logger.error(f"Error validating upload: {str(e)}")
        return False, f'Error validating file: {str(e)}'