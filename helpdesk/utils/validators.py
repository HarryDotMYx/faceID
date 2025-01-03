  
from django.core.exceptions import ValidationError

def validate_complaint_title(title):
    if len(title) < 5:
        raise ValidationError("Title must be at least 5 characters long")
    if len(title) > 200:
        raise ValidationError("Title must not exceed 200 characters")

def validate_complaint_description(description):
    if len(description) < 20:
        raise ValidationError("Description must be at least 20 characters long")
  