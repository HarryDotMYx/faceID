from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..utils.face_processing import process_uploaded_face
from ..train import train_user_model
from ..models import FaceImage
from .validators import validate_upload
import logging

logger = logging.getLogger(__name__)

@login_required
@csrf_exempt
def process_upload(request):
    """Process uploaded face image"""
    try:
        if 'image' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No image provided'})
        
        # Validate upload
        image = request.FILES['image']
        is_valid, error = validate_upload(image)
        if not is_valid:
            return JsonResponse({'success': False, 'error': error})
        
        # Create face image
        face_image = FaceImage.objects.create(
            user=request.user,
            image=image
        )
        
        # Process and validate face
        success, message = process_uploaded_face(face_image.image.path, request.user.id)
        
        if success:
            # Train model with new image
            train_success, train_message = train_user_model(request.user.id)
            if train_success:
                return JsonResponse({'success': True})
            else:
                face_image.delete()
                return JsonResponse({'success': False, 'error': train_message})
        else:
            face_image.delete()
            return JsonResponse({'success': False, 'error': message})
            
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})