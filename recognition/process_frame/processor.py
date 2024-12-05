from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import logging
from .validators import validate_request
from .frame_handler import FrameHandler
from ..utils.response_helpers import error_response, success_response

logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def process_frame(request):
    """Process video frame for face detection"""
    try:
        # Validate request and get frame data
        validation_result = validate_request(request)
        if not validation_result['valid']:
            return error_response(validation_result['error'])

        # Process frame
        frame_handler = FrameHandler(request.user)
        faces = frame_handler.process(request.FILES['frame'])
        
        # Return results
        return success_response({'faces': faces})
        
    except Exception as e:
        logger.error(f"Error processing frame: {str(e)}", exc_info=True)
        return error_response('Internal server error', status=500)