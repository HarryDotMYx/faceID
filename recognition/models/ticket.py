from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('open', 'Open'), 
        ('review', 'Under Review'),
        ('hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed')
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'Technical Issue'),
        ('account', 'Account Related'),
        ('feature', 'Feature Request'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    response = models.TextField(blank=True, null=True)
    
    # Time tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Status tracking
    status_changed_at = models.DateTimeField(null=True, blank=True)
    previous_status = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.subject} - {self.user.username}"
        
    def save(self, *args, **kwargs):
        # Track status changes
        if self.pk:
            old_ticket = Ticket.objects.get(pk=self.pk)
            if old_ticket.status != self.status:
                self.previous_status = old_ticket.status
                self.status_changed_at = timezone.now()
                
                # Set closed_at when status changes to closed
                if self.status == 'closed' and old_ticket.status != 'closed':
                    self.closed_at = timezone.now()
                # Clear closed_at if reopened
                elif self.status != 'closed' and old_ticket.status == 'closed':
                    self.closed_at = None
                    
        super().save(*args, **kwargs)
        
    @property
    def days_open(self):
        """Calculate days ticket has been open"""
        if self.closed_at:
            return (self.closed_at - self.created_at).days
        return (timezone.now() - self.created_at).days
        
    @property
    def month_created(self):
        """Get month ticket was created"""
        return self.created_at.strftime('%B')
        
    @property
    def year_created(self):
        """Get year ticket was created"""
        return self.created_at.year