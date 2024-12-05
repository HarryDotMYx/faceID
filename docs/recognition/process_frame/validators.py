from ..models import FaceImage

def validate_request(request):
    """Validate frame processing request"""
    # Check if user has uploaded face images
    if not FaceImage.objects.filter(user=request.user).exists():
        return {
            'valid': False,
            'error': 'No face images found. Please upload face images first.'
        }

    # Check frame data
    if 'frame' not in request.FILES:
        return {
            'valid': False,
            'error': 'No frame data provided'
        }

    return {
        'valid': True,
        'error': None
    }