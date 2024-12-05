from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('blue', 'Blue'),
        ('green', 'Green'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    bio = models.TextField(max_length=500, blank=True)
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_theme_class(self):
        return {
            'light': 'bg-white',
            'dark': 'bg-gray-900',
            'blue': 'bg-blue-50',
            'green': 'bg-green-50'
        }.get(self.theme, 'bg-white')