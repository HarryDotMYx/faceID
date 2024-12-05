from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import FaceImage
from .utils.face_processing import process_uploaded_face
from .utils.face_verification import verify_face
from .utils.frame_processor import FrameProcessor
from .train import train_user_model

logger = logging.getLogger(__name__)

@login_required
def process_frame(request):
    """Process video frame for face detection"""
    if request.method == 'POST' and request.FILES.get('frame'):
        try:
            frame_data = request.FILES['frame']
            processor = FrameProcessor()
            faces = processor.process_frame(frame_data, request.user.id, request.user.username)
            return JsonResponse({'faces': faces})
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def live_recognition(request):
    """Live face recognition view"""
    has_faces = FaceImage.objects.filter(user=request.user).exists()
    if not has_faces:
        messages.warning(request, 'Please upload some face images before using live recognition.')
    return render(request, 'recognition/live.html', {
        'has_faces': has_faces,
        'username': request.user.username
    })