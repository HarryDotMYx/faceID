import face_recognition
import pickle
from .file_handlers import get_user_paths

def verify_face(image_path, user_id):
    """Verify if the face matches the stored encoding"""
    # Get user paths
    user_paths = get_user_paths(user_id)
    encoding_path = user_paths['encoding']
    
    try:
        # Check if user has stored encodings
        with open(encoding_path, "rb") as f:
            data = pickle.loads(f.read())
            
        if not data["encodings"]:
            return False, "No stored face encodings found"
        
        # Load and process the verification image
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            return False, "No face detected in the verification image"
        
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        if not face_encodings:
            return False, "Could not encode face features"
        
        # Compare faces
        matches = face_recognition.compare_faces(
            data["encodings"],
            face_encodings[0],
            tolerance=0.6
        )
        
        if True in matches:
            return True, "Face verified successfully"
        else:
            return False, "Face verification failed - no match found"
            
    except FileNotFoundError:
        return False, "No stored face encodings found"
    except Exception as e:
        return False, f"Verification error: {str(e)}"