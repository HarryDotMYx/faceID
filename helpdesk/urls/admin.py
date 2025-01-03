  
from django.urls import path
from ..views.admin import dashboard, complaint_management

app_name = 'admin'

urlpatterns = [
    path('', dashboard.admin_dashboard, name='dashboard'),
    path('complaints/', complaint_management.complaint_list, name='complaint_list'),
    path('complaints/<int:complaint_id>/', complaint_management.complaint_detail, name='complaint_detail'),
]
  