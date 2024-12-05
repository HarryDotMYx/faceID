import cv2
import numpy as np
from PIL import Image
import logging

def validate_image_quality(image_path):
    """Validate image quality for face detection"""
    try:
        # Open image with PIL
        image = Image.open(image_path)
        
        # Check image dimensions
        width, height = image.size
        if width < 160 or height < 160:
            return False, "Image resolution is too low. Please use an image at least 160x160 pixels."
        
        # Convert to numpy array for OpenCV processing
        img_array = np.array(image)
        
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Check brightness
        brightness = np.mean(gray)
        if brightness < 15:  # More lenient dark threshold
            return False, "Image is too dark. Please use a better lit photo."
        if brightness > 250:
            return False, "Image is too bright. Please use a photo with better contrast."
        
        # Check contrast
        contrast = np.std(gray)
        if contrast < 5:  # More lenient contrast threshold
            return False, "Image has very low contrast. Please use a clearer photo."
        
        # Check blur
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 20:  # More lenient blur threshold
            return False, "Image appears to be blurry. Please use a sharper, clearer photo."
        
        return True, "Image quality is acceptable"
        
    except Exception as e:
        logging.error(f"Error validating image quality: {str(e)}")
        return False, "Error validating image quality. Please try another image."