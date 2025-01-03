  
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..services.frame_processing_service import FrameProcessingService
from ..models import FaceImage
from ..utils.response_helpers import error_response, success_response

@login_required
@csrf_exempt
def process_frame(request):
    """Process video frame for face detection"""
    try:
        # Validate user has face images
        if not FaceImage.objects.filter(user=request.user).exists():
            return error_response('No face images found. Please upload face images first.')

        # Get frame data
        frame_data = request.FILES.get('frame')
        if not frame_data:
            return error_response('No frame data provided')

        # Initialize service
        service = FrameProcessingService()
        if not service.initialize(request.user.id, request.user.username):
            return error_response('Failed to load face encodings')
            
        # Process frame
        faces = service.process_frame(frame_data)
        
        return success_response({'faces': faces})
        
    except Exception as e:
        return error_response(str(e), status=500)
  