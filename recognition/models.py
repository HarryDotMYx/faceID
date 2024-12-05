from django.db import models
from django.contrib.auth.models import User
from .utils.file_validation import validate_image_file

class FaceImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='face_images',
        validators=[validate_image_file]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.uploaded_at}'

    class Meta:
        ordering = ['-uploaded_at']