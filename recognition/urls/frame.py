from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from recognition.views.frame_processing import process_frame

app_name = 'frame'

urlpatterns = [
    path('', csrf_exempt(process_frame), name='process'),
]