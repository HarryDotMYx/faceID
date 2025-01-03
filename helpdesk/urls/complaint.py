  
from django.urls import path
from ..views.user import complaint_views

urlpatterns = [
    path('add/', complaint_views.add_complaint, name='add_complaint'),
    path('<int:complaint_id>/', complaint_views.view_complaint, name='view_complaint'),
    path('<int:complaint_id>/reply/', complaint_views.add_reply, name='add_reply'),
]
  