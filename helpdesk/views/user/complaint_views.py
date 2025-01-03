  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ...models import Complaint
from ...forms import ComplaintForm, ComplaintReplyForm

@login_required
def add_complaint(request):
    """Add a new complaint"""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Your complaint has been submitted.')
            return redirect('helpdesk:view_complaint', complaint_id=complaint.id)
    else:
        form = ComplaintForm()
    
    return render(request, 'helpdesk/user/add_complaint.html', {'form': form})

@login_required
def view_complaint(request, complaint_id):
    """View a specific complaint"""
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    reply_form = ComplaintReplyForm()
    
    return render(request, 'helpdesk/user/view_complaint.html', {
        'complaint': complaint,
        'reply_form': reply_form
    })

@login_required
def add_reply(request, complaint_id):
    """Add a reply to a complaint"""
    complaint = get_object_or_404(Complaint, id=complaint_id, user=request.user)
    
    if request.method == 'POST':
        form = ComplaintReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.complaint = complaint
            reply.user = request.user
            reply.save()
            messages.success(request, 'Your reply has been added.')
            
    return redirect('helpdesk:view_complaint', complaint_id=complaint_id)
  