from django.core.exceptions import ValidationError
import magic
import logging

logger = logging.getLogger(__name__)

def validate_frame_data(frame_data):
    """Validate uploaded frame data"""
    try:
        # Check file size (max 5MB)
        if frame_data.size > 5 * 1024 * 1024:
            raise ValidationError('Frame data too large')
            
        # Check MIME type
        mime = magic.from_buffer(frame_data.read(1024), mime=True)
        frame_data.seek(0)  # Reset file pointer
        
        if not mime.startswith('image/'):
            raise ValidationError('Invalid frame data format')
            
    except Exception as e:
        logger.error(f"Error validating frame data: {str(e)}")
        raise ValidationError('Invalid frame data')