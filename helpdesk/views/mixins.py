  
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ComplaintAccessMixin:
    def check_complaint_access(self, complaint):
        user = self.request.user
        if not user.is_staff and complaint.user != user:
            raise PermissionDenied("You don't have permission to access this complaint")
  