from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from recognition.process_frame.processor import process_frame

app_name = 'frame'

urlpatterns = [
    path('', csrf_exempt(process_frame), name='process'),
]