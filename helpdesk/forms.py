  
from django import forms
from .models import Complaint, ComplaintReply

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ComplaintReplyForm(forms.ModelForm):
    class Meta:
        model = ComplaintReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class ComplaintUpdateForm(forms.Form):
    STATUS_CHOICES = Complaint.STATUS_CHOICES

    status = forms.ChoiceField(choices=STATUS_CHOICES)
    assigned_to = forms.ModelChoiceField(
        queryset=None,  # Set in __init__
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)
  