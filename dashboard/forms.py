from django import forms
from django.forms import ModelForm
from Email.models import Email


# class EmailForm(forms.Form):
#     sender_email = forms.EmailField(label='From:', disabled=False)
#     recipient_email = forms.EmailField(label='To:')
#     subject = forms.CharField(max_length=1000, label='Subject:')
#     body = forms.CharField(widget=forms.Textarea, label='Message:')

class EmailForm(ModelForm):
    class Meta:
        model = Email
        fields = ['sender_email', 'recipient_email', 'subject', 'body', 'image']
        widgets = {
            'sender_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'From:', 'disabled': False}),
            'recipient_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'To:'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject:'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message:'}),
        }