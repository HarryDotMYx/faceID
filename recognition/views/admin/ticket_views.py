from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from ...models import Ticket
from .utils import is_admin, get_filtered_tickets

@user_passes_test(is_admin)
def admin_tickets(request):
    """View all tickets with filters"""
    tickets = get_filtered_tickets(request)
    
    context = {
        'tickets': tickets,
        'status_choices': Ticket.STATUS_CHOICES,
        'current_status': request.GET.get('status'),
        'current_month': request.GET.get('month'),
        'current_year': request.GET.get('year'),
    }
    return render(request, 'recognition/admin/tickets.html', context)

@user_passes_test(is_admin)
def update_ticket(request, ticket_id):
    """Update ticket status and response"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        response = request.POST.get('response')
        
        if new_status:
            ticket.status = new_status
            if response:
                ticket.response = response
            ticket.save()
            
            messages.success(request, f'Ticket status updated to {ticket.get_status_display()}')
            return redirect('recognition:admin:tickets')
            
    return render(request, 'recognition/admin/update_ticket.html', {
        'ticket': ticket,
        'status_choices': Ticket.STATUS_CHOICES
    })

@user_passes_test(is_admin)
def delete_ticket(request, ticket_id):
    """Delete a ticket"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Ticket deleted successfully')
        return redirect('recognition:admin:tickets')
        
    return render(request, 'recognition/admin/delete_ticket.html', {'ticket': ticket})