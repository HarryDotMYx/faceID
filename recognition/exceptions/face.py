from .base import RecognitionError

class FaceDetectionError(RecognitionError):
    """Raised when face detection fails"""
    def __init__(self, message="Failed to detect faces in the image"):
        super().__init__(message)

class FaceEncodingError(RecognitionError):
    """Raised when face encoding fails"""
    def __init__(self, message="Failed to encode face features"):
        super().__init__(message)

class FaceValidationError(RecognitionError):
    """Raised when face validation fails"""
    def __init__(self, message="Face validation failed"):
        super().__init__(message)

class NoFaceDetectedError(RecognitionError):
    """Raised when no face is detected in the image"""
    def __init__(self, message="No face detected in the image"):
        super().__init__(message)