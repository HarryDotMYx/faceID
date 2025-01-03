from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('subject', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if change and 'response' in form.changed_data:
            obj.status = 'closed'  # Auto-close ticket when response is added
        super().save_model(request, obj, form, change)