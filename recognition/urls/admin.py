from django.urls import path
from recognition.views.admin import (
    admin_tickets,
    update_ticket,
    delete_ticket,
    ticket_stats
)

app_name = 'admin'

urlpatterns = [
    path('tickets/', admin_tickets, name='tickets'),
    path('tickets/<int:ticket_id>/update/', update_ticket, name='update_ticket'),
    path('tickets/<int:ticket_id>/delete/', delete_ticket, name='delete_ticket'),
    path('tickets/stats/', ticket_stats, name='ticket_stats'),
]