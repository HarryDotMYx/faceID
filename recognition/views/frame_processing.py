from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..utils.frame_processor import FrameProcessor
from ..models import FaceImage

@login_required
@csrf_exempt
def process_frame(request):
    """Process video frame for face detection"""
    try:
        # Check if user has uploaded face images
        if not FaceImage.objects.filter(user=request.user).exists():
            return JsonResponse({
                'success': False,
                'error': 'No face images found. Please upload face images first.'
            })

        # Get frame data
        frame_data = request.FILES.get('frame')
        if not frame_data:
            return JsonResponse({
                'success': False,
                'error': 'No frame data provided'
            })

        # Process frame
        processor = FrameProcessor()
        if not processor.load_encodings(request.user.id):
            return JsonResponse({
                'success': False,
                'error': 'Failed to load face encodings'
            })
            
        faces = processor.process_frame(frame_data, request.user.id, request.user.username)
        
        return JsonResponse({
            'success': True,
            'faces': faces
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)