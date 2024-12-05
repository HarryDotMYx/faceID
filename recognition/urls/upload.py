from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from recognition.views.upload import process_upload

app_name = 'upload'

urlpatterns = [
    path('process/', csrf_exempt(process_upload), name='process'),
]