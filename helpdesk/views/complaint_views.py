  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import ComplaintForm, ComplaintReplyForm
from ..services.complaint_service import ComplaintService

@login_required
def add_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = ComplaintService.create_complaint(
                user=request.user,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description']
            )
            messages.success(request, 'Complaint submitted successfully!')
            return redirect('helpdesk:view_complaint', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    
    return render(request, 'helpdesk/add_complaint.html', {'form': form})

@login_required
def view_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        form = ComplaintReplyForm(request.POST)
        if form.is_valid():
            ComplaintService.add_reply(
                complaint_id=complaint.id,
                user=request.user,
                message=form.cleaned_data['message']
            )
            messages.success(request, 'Reply added successfully!')
            return redirect('helpdesk:view_complaint', complaint_id=complaint.id)
    else:
        form = ComplaintReplyForm()
    
    return render(request, 'helpdesk/view_complaint.html', {
        'complaint': complaint,
        'form': form
    })
  