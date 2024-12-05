from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    """Home page view"""
    context = {
        'title': 'Face Recognition System',
        'user': request.user
    }
    return render(request, 'recognition/home.html', context)