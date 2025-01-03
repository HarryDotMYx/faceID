from ...models import Ticket

def create_ticket(request):
    """Create a new support ticket"""
    return Ticket.objects.create(
        user=request.user,
        subject=request.POST['subject'],
        category=request.POST['category'],
        description=request.POST['description']
    )