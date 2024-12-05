import cv2
import numpy as np
import face_recognition
from django.conf import settings
import os

def process_and_save_face(image_path, user_id):
    """Process uploaded image and save face encoding"""
    # Load the uploaded image
    image = face_recognition.load_image_file(image_path)
    
    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        return False, "No face detected in the image"
    
    # Get face encodings
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    if not face_encodings:
        return False, "Could not encode face features"
    
    # Save the face encoding
    encoding_path = os.path.join(settings.MEDIA_ROOT, f'encodings/user_{user_id}.npy')
    os.makedirs(os.path.dirname(encoding_path), exist_ok=True)
    np.save(encoding_path, face_encodings[0])
    
    return True, "Face processed successfully"

def verify_face(image_path, user_id):
    """Verify if the face matches the stored encoding"""
    # Load the stored encoding
    encoding_path = os.path.join(settings.MEDIA_ROOT, f'encodings/user_{user_id}.npy')
    
    if not os.path.exists(encoding_path):
        return False, "No stored face encoding found"
    
    stored_encoding = np.load(encoding_path)
    
    # Load and process the new image
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        return False, "No face detected in the image"
    
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    if not face_encodings:
        return False, "Could not encode face features"
    
    # Compare faces
    matches = face_recognition.compare_faces([stored_encoding], face_encodings[0])
    
    if matches[0]:
        return True, "Face verified successfully"
    else:
        return False, "Face verification failed"