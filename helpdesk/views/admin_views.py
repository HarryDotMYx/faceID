  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from ..models import Complaint
from ..services.complaint_service import ComplaintService
from ..forms import ComplaintUpdateForm, ComplaintReplyForm

@user_passes_test(lambda u: u.is_staff)
def admin_complaints(request):
    complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'helpdesk/admin/complaints.html', {
        'complaints': complaints
    })

@user_passes_test(lambda u: u.is_staff)
def update_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintUpdateForm(request.POST)
        if form.is_valid():
            ComplaintService.update_complaint(
                complaint_id=complaint.id,
                status=form.cleaned_data['status'],
                assigned_to=form.cleaned_data['assigned_to'],
                user=request.user
            )
            messages.success(request, 'Complaint updated successfully!')
            return redirect('helpdesk:admin_view_complaint', complaint_id=complaint.id)
    else:
        form = ComplaintUpdateForm(initial={
            'status': complaint.status,
            'assigned_to': complaint.assigned_to
        })
    
    return render(request, 'helpdesk/admin/update_complaint.html', {
        'complaint': complaint,
        'form': form
    })
  