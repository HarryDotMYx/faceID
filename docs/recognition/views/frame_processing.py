from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging
from ..utils.frame_processor import FrameProcessor
from ..utils.response_helpers import error_response, success_response
from ..models import FaceImage

logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def process_frame(request):
    """Process video frame for face detection"""
    try:
        # Check if user has uploaded face images
        if not FaceImage.objects.filter(user=request.user).exists():
            return error_response('No face images found. Please upload face images first.')

        # Get frame data
        frame_data = request.FILES.get('frame')
        if not frame_data:
            return error_response('No frame data provided')

        # Initialize processor
        processor = FrameProcessor()
        
        # Load user's face encodings
        if not processor.load_encodings(request.user.id):
            return error_response('No face encodings found. Please upload face images first.')
            
        # Process the frame
        faces = processor.process_frame(frame_data, request.user.id, request.user.username)
        
        # Return results
        return success_response({'faces': faces})
        
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}", exc_info=True)
        return error_response('Internal server error', status=500)