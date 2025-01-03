from django.urls import path, include

app_name = 'recognition'

urlpatterns = [
    path('', include('recognition.urls.main')),
    path('face/', include(('recognition.urls.face', 'face'))),
    path('webcam/', include(('recognition.urls.webcam', 'webcam'))),
    path('process-frame/', include('recognition.urls.frame')),
    path('helpdesk/', include(('recognition.urls.helpdesk', 'helpdesk'))),
    path('admin/', include(('recognition.urls.admin', 'admin'))),
]