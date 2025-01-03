from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models.helpdesk import Ticket

@login_required
def helpdesk(request):
    if request.method == 'POST':
        ticket = Ticket.objects.create(
            user=request.user,
            subject=request.POST['subject'],
            category=request.POST['category'],
            description=request.POST['description']
        )
        messages.success(request, 'Support ticket submitted successfully!')
        return redirect('recognition:helpdesk')
        
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'recognition/helpdesk.html', {'tickets': tickets})