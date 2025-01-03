from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ...models import Ticket

@login_required
def helpdesk_home(request):
    """Main helpdesk view for submitting tickets and viewing history"""
    if request.method == 'POST':
        ticket = Ticket.objects.create(
            user=request.user,
            subject=request.POST['subject'],
            category=request.POST['category'],
            description=request.POST['description']
        )
        messages.success(request, 'Support ticket submitted successfully!')
        return redirect('recognition:helpdesk:home')
        
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'recognition/helpdesk.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    """Handle ticket creation"""
    if request.method == 'POST':
        ticket = Ticket.objects.create(
            user=request.user,
            subject=request.POST['subject'],
            category=request.POST['category'],
            description=request.POST['description']
        )
        messages.success(request, 'Support ticket submitted successfully!')
        return redirect('recognition:helpdesk:view', ticket_id=ticket.id)
    return redirect('recognition:helpdesk:home')

@login_required
def view_ticket(request, ticket_id):
    """View a specific ticket's details"""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, 'recognition/helpdesk/ticket_detail.html', {'ticket': ticket})

@login_required
def list_tickets(request):
    """View all tickets for the user"""
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'recognition/helpdesk/ticket_list.html', {'tickets': tickets})