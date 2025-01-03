from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.utils import timezone
from ...models import Ticket

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_tickets(request):
    """View all tickets with filters"""
    status_filter = request.GET.get('status')
    month_filter = request.GET.get('month')
    year_filter = request.GET.get('year')
    
    tickets = Ticket.objects.all()
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    if month_filter:
        tickets = tickets.filter(created_at__month=month_filter)
    if year_filter:
        tickets = tickets.filter(created_at__year=year_filter)
        
    tickets = tickets.order_by('-created_at')
    
    context = {
        'tickets': tickets,
        'status_choices': Ticket.STATUS_CHOICES,
        'current_status': status_filter,
        'current_month': month_filter,
        'current_year': year_filter,
    }
    return render(request, 'recognition/admin/tickets.html', context)

@user_passes_test(is_admin)
def update_ticket_status(request, ticket_id):
    """Update ticket status"""
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
def ticket_stats(request):
    """View detailed ticket statistics"""
    stats = {
        'total': Ticket.objects.count(),
        'status_counts': {
            status: Ticket.objects.filter(status=status_code).count()
            for status_code, status in Ticket.STATUS_CHOICES
        },
        'by_month': Ticket.objects.extra(
            select={'month': "EXTRACT(month FROM created_at)"}
        ).values('month').annotate(count=Count('id')),
        'by_year': Ticket.objects.extra(
            select={'year': "EXTRACT(year FROM created_at)"}
        ).values('year').annotate(count=Count('id')),
        'avg_days_open': Ticket.objects.filter(
            closed_at__isnull=False
        ).extra(
            select={'days_open': "EXTRACT(day FROM (closed_at - created_at))"}
        ).values('days_open').aggregate(avg_days=models.Avg('days_open'))
    }
    return render(request, 'recognition/admin/ticket_stats.html', {'stats': stats})