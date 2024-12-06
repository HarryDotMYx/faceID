class UserInactiveError(Exception):
    """Raised when user account is inactive"""
    def __init__(self, message="Your account is not activated. Please check your email for activation instructions."):
        self.message = message
        super().__init__(self.message)

class UserBannedError(Exception):
    """Raised when user account is banned"""
    def __init__(self, message="Your account has been banned. Please contact support for assistance."):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid"""
    def __init__(self, message="Invalid username or password."):
        self.message = message
        super().__init__(self.message)