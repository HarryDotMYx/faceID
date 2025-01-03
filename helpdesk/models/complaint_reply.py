  
from django.db import models
from django.contrib.auth.models import User
from .complaint import Complaint

class ComplaintReply(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff_reply = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Complaint replies'

    def __str__(self):
        return f"Reply to {self.complaint.title} by {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.is_staff_reply = self.user.is_staff
        super().save(*args, **kwargs)
  