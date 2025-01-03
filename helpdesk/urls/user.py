  
from django.urls import path
from ..views.user import dashboard, complaint_views

urlpatterns = [
    path('', dashboard.user_dashboard, name='dashboard'),
    path('complaint/add/', complaint_views.add_complaint, name='add_complaint'),
    path('complaint/<int:complaint_id>/', complaint_views.view_complaint, name='view_complaint'),
    path('complaint/<int:complaint_id>/reply/', complaint_views.add_reply, name='add_reply'),
]
  