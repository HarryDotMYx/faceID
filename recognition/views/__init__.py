from .home import home
from .face import upload_face, verify, delete_face
from .webcam import webcam_capture, save_webcam_image, live_recognition

__all__ = [
    'home',
    'upload_face',
    'verify', 
    'delete_face',
    'webcam_capture',
    'save_webcam_image',
    'live_recognition'
]