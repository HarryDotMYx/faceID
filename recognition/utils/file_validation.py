import os
from django.core.exceptions import ValidationError
import magic
import logging

def validate_file_size(file):
    """Validate file size (max 5MB)"""
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    
    if file.size > max_size:
        raise ValidationError(f'File size must not exceed 5MB. Current size: {file.size / (1024 * 1024):.2f}MB')

def validate_file_extension(file):
    """Validate file extension and MIME type"""
    valid_extensions = ['.jpg', '.jpeg', '.png']
    valid_mimetypes = ['image/jpeg', 'image/png']
    
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Please use: {", ".join(valid_extensions)}')
    
    # Check MIME type
    try:
        file_mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)  # Reset file pointer
        
        if file_mime not in valid_mimetypes:
            raise ValidationError('Invalid image format. Please upload a valid JPEG or PNG file.')
    except Exception as e:
        logging.error(f"Error validating file type: {str(e)}")
        raise ValidationError('Could not validate file type. Please try again.')

def validate_image_file(file):
    """Validate both file size and type"""
    validate_file_size(file)
    validate_file_extension(file)