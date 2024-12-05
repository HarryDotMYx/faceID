from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserUpdateForm, ProfileUpdateForm
from recognition.models import FaceImage

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    face_images = FaceImage.objects.filter(user=request.user).order_by('-uploaded_at')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'face_images': face_images,
        'theme_class': request.user.profile.get_theme_class()
    }
    return render(request, 'users/profile.html', context)