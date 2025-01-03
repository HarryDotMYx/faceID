def is_admin(user):
    """Check if user is admin"""
    return user.is_staff

def get_filtered_tickets(request):
    """Get tickets based on filters"""
    from ...models import Ticket
    
    tickets = Ticket.objects.all()
    
    status = request.GET.get('status')
    month = request.GET.get('month')
    year = request.GET.get('year')
    
    if status:
        tickets = tickets.filter(status=status)
    if month:
        tickets = tickets.filter(created_at__month=month)
    if year:
        tickets = tickets.filter(created_at__year=year)
        
    return tickets.order_by('-created_at')