from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from ..models import FaceImage
from ..utils.face_processing import process_uploaded_face
from ..train import train_user_model

@login_required
def webcam_capture(request):
    """Webcam capture view"""
    return render(request, 'recognition/webcam_capture.html')

@login_required
def save_webcam_image(request):
    """Save image captured from webcam"""
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