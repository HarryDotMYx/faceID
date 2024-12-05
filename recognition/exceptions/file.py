from .base import RecognitionError

class FileValidationError(RecognitionError):
    """Base exception for file validation errors"""
    def __init__(self, message="File validation failed"):
        super().__init__(message)

class FileSizeError(FileValidationError):
    """Raised when file size exceeds limit"""
    def __init__(self, message="File size exceeds maximum limit"):
        super().__init__(message)

class FileTypeError(FileValidationError):
    """Raised when file type is not supported"""
    def __init__(self, message="File type not supported"):
        super().__init__(message)