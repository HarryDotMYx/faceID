from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import FaceImage
from ..utils.face_processing import process_uploaded_face
from ..utils.face_verification import verify_face
from ..train import train_user_model

@login_required
def upload_face(request):
    """Handle face image upload"""
    if request.method == 'POST':
        if 'image' in request.FILES:
            image = request.FILES['image']
            
            face_image = FaceImage.objects.create(
                user=request.user,
                image=image
            )
            
            success, message = process_uploaded_face(face_image.image.path, request.user.id)
            
            if success:
                train_success, train_message = train_user_model(request.user.id)
                if train_success:
                    messages.success(request, 'Face image uploaded and model trained successfully!')
                else:
                    messages.warning(request, f'Image uploaded but training failed: {train_message}')
            else:
                messages.error(request, message)
                face_image.delete()
            
            return redirect('recognition:face:upload')
    
    face_images = FaceImage.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'recognition/upload.html', {'face_images': face_images})

@login_required
def verify(request):
    """Handle face verification"""
    if request.method == 'POST':
        if 'image' in request.FILES:
            temp_image = FaceImage.objects.create(
                user=request.user,
                image=request.FILES['image']
            )
            
            success, message = verify_face(temp_image.image.path, request.user.id)
            temp_image.delete()
            
            if success:
                messages.success(request, 'Face verified successfully!')
            else:
                messages.error(request, f'Verification failed: {message}')
            
            return redirect('recognition:face:verify')
    return render(request, 'recognition/verify.html')

@login_required
def delete_face(request, image_id):
    """Delete face image"""
    if request.method == 'POST':
        face_image = get_object_or_404(FaceImage, id=image_id, user=request.user)
        face_image.delete()
        
        train_success, train_message = train_user_model(request.user.id)
        if not train_success:
            messages.warning(request, f'Image deleted but training failed: {train_message}')
            
    return redirect('recognition:face:upload')