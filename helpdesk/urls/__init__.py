  
from django.urls import path, include

app_name = 'helpdesk'

urlpatterns = [
    # User routes
    path('', include('helpdesk.urls.user')),
    path('admin/', include('helpdesk.urls.admin')),
]
  