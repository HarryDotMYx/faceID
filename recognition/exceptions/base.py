class RecognitionError(Exception):
    """Base exception for all recognition related errors"""
    def __init__(self, message="An error occurred in the recognition system"):
        self.message = message
        super().__init__(self.message)