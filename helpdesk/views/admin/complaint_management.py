  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from ...models import Complaint
from ...forms import ComplaintUpdateForm

@user_passes_test(lambda u: u.is_staff)
def complaint_list(request):
    """List all complaints with filtering options"""
    status_filter = request.GET.get('status', '')
    complaints = Complaint.objects.all()
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
        
    complaints = complaints.order_by('-created_at')
    return render(request, 'helpdesk/admin/complaint_list.html', {
        'complaints': complaints,
        'status_filter': status_filter
    })

@user_passes_test(lambda u: u.is_staff)
def complaint_detail(request, complaint_id):
    """Detailed view of a complaint with update form"""
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintUpdateForm(request.POST)
        if form.is_valid():
            complaint.status = form.cleaned_data['status']
            complaint.assigned_to = form.cleaned_data['assigned_to']
            complaint.save()
            messages.success(request, 'Complaint updated successfully')
            return redirect('helpdesk:admin:complaint_list')
    else:
        form = ComplaintUpdateForm(initial={
            'status': complaint.status,
            'assigned_to': complaint.assigned_to
        })
    
    return render(request, 'helpdesk/admin/complaint_detail.html', {
        'complaint': complaint,
        'form': form
    })
  