from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Avg
from ...models import Ticket
from .utils import is_admin

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
        ).values('days_open').aggregate(avg_days=Avg('days_open'))
    }
    return render(request, 'recognition/admin/ticket_stats.html', {'stats': stats})