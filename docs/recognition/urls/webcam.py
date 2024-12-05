from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from recognition.views.webcam import webcam_capture, save_webcam_image, live_recognition

app_name = 'webcam'

urlpatterns = [
    path('capture/', webcam_capture, name='capture'),
    path('save/', csrf_exempt(save_webcam_image), name='save'),
    path('live/', live_recognition, name='live'),
]