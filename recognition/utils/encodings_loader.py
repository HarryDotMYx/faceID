import pickle
import logging
from .file_handlers import get_user_paths

logger = logging.getLogger(__name__)

def load_user_encodings(user_id):
    """Load face encodings for a user"""
    try:
        user_paths = get_user_paths(user_id)
        with open(user_paths['encoding'], 'rb') as f:
            data = pickle.loads(f.read())
            return data["encodings"]
    except Exception as e:
        logger.error(f"Error loading user encodings: {str(e)}")
        return None