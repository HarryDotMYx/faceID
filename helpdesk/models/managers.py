  
from django.db import models

class ComplaintManager(models.Manager):
    def get_active_complaints(self):
        return self.exclude(status__in=['resolved', 'closed'])
    
    def get_user_complaints(self, user):
        return self.filter(user=user)
    
    def get_staff_assigned(self, staff_user):
        return self.filter(assigned_to=staff_user)
  