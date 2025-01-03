from django.urls import path
from recognition.views.helpdesk.views import (
    helpdesk_home,
    create_ticket,
    view_ticket,
    list_tickets
)

app_name = 'helpdesk'

urlpatterns = [
    path('', helpdesk_home, name='home'),
    path('create/', create_ticket, name='create'),
    path('tickets/', list_tickets, name='list'),
    path('ticket/<int:ticket_id>/', view_ticket, name='view'),
]