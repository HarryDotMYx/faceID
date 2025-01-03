  
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from ...models import Complaint

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Admin dashboard showing complaint statistics and recent items"""
    new_complaints = Complaint.objects.filter(status='new').count()
    in_progress = Complaint.objects.filter(status='in_progress').count()
    resolved = Complaint.objects.filter(status='resolved').count()
    recent_complaints = Complaint.objects.order_by('-created_at')[:5]
    
    context = {
        'new_complaints': new_complaints,
        'in_progress': in_progress,
        'resolved': resolved,
        'recent_complaints': recent_complaints
    }
    return render(request, 'helpdesk/admin/dashboard.html', context)
  