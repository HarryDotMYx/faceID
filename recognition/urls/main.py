from django.urls import path
from recognition.views.home import home

app_name = 'main'

urlpatterns = [
    path('', home, name='home'),
]