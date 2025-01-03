from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FaceImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='face_images')
    uploaded_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    recognition_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f'{self.user.username} - {self.uploaded_at}'
        
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)