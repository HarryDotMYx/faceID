from django.urls import path
from recognition.views.reports import generate_report

app_name = 'reports'

urlpatterns = [
    path('generate/', generate_report, name='generate'),
]