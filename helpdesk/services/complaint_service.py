  
from django.core.exceptions import PermissionDenied
from ..models import Complaint, ComplaintReply

class ComplaintService:
    @staticmethod
    def create_complaint(user, title, description):
        return Complaint.objects.create(
            user=user,
            title=title,
            description=description
        )

    @staticmethod
    def add_reply(complaint_id, user, message):
        complaint = Complaint.objects.get(id=complaint_id)
        
        if not user.is_staff and complaint.user != user:
            raise PermissionDenied("You don't have permission to reply")
            
        return ComplaintReply.objects.create(
            complaint=complaint,
            user=user,
            message=message,
            is_staff_reply=user.is_staff
        )

    @staticmethod
    def update_status(complaint_id, status, assigned_to=None, user=None):
        complaint = Complaint.objects.get(id=complaint_id)
        
        if not user.is_staff:
            raise PermissionDenied("Only staff can update complaint status")
            
        complaint.status = status
        if assigned_to:
            complaint.assigned_to = assigned_to
        complaint.save()
        return complaint
  