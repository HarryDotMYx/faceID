from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..models import FaceImage
from ..utils.face_processing import process_uploaded_face
from ..train import train_user_model

@login_required
@csrf_exempt
def process_upload(request):
    """Process uploaded face image"""
    if request.method == 'POST':
        try:
            if 'image' not in request.FILES:
                return JsonResponse({'success': False, 'error': 'No image provided'})
            
            image = request.FILES['image']
            face_image = FaceImage.objects.create(
                user=request.user,
                image=image
            )
            
            success, message = process_uploaded_face(face_image.image.path, request.user.id)
            
            if success:
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
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})