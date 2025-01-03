  
from django.urls import path, include
from .views.user import dashboard as user_dashboard
from .views.admin import dashboard as admin_dashboard

app_name = 'helpdesk'

urlpatterns = [
    # User routes
    path('', user_dashboard.user_dashboard, name='dashboard'),
    path('complaint/', include('helpdesk.urls.complaint')),
    
    # Admin routes
    path('admin/', include('helpdesk.urls.admin', namespace='admin')),
]
  