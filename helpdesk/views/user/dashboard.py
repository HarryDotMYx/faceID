
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ...models import Complaint

@login_required
def user_dashboard(request):
    """User dashboard showing their complaints and status"""
    user_complaints = Complaint.objects.filter(user=request.user)
    
    # Get counts by status
    new_count = user_complaints.filter(status='new').count()
    in_progress_count = user_complaints.filter(status='in_progress').count()
    resolved_count = user_complaints.filter(status='resolved').count()
    
    # Get recent complaints
    recent_complaints = user_complaints.order_by('-created_at')[:5]
    
    context = {
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'recent_complaints': recent_complaints,
        'total_complaints': user_complaints.count()
    }
    return render(request, 'helpdesk/user/dashboard.html', context)
  