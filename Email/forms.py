from django import forms

class EmailForm(forms.Form):
    sender_email = forms.EmailField(label='From:', disabled=False)
    recipient_email = forms.EmailField(label='To:')
    subject = forms.CharField(max_length=1000, label='Subject:')
    body = forms.CharField(widget=forms.Textarea, label='Message:')