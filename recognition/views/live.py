from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import FaceImage

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