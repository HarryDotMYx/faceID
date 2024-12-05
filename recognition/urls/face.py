from django.urls import path
from recognition.views.face import upload_face, verify, delete_face

app_name = 'face'

urlpatterns = [
    path('upload/', upload_face, name='upload'),
    path('verify/', verify, name='verify'),
    path('delete/<int:image_id>/', delete_face, name='delete'),
]