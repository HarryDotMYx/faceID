from django.urls import path, include

app_name = 'recognition'

urlpatterns = [
    path('', include('recognition.urls.main')),
    path('face/', include('recognition.urls.face')),
    path('webcam/', include('recognition.urls.webcam')),
    path('process-frame/', include('recognition.urls.frame')),
    path('upload/', include('recognition.urls.upload')),
    path('reports/', include('recognition.urls.reports')),
]