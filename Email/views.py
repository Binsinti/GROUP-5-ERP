from django.shortcuts import render, redirect
from .forms import *
from django.core.mail import send_mail



# Create your views here.

def email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            recipient_email = form.cleaned_data['recipient_email']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            sender_email = request.user.email

            try:
                send_mail(
                    subject,
                    body,  # The body of the email
                    sender_email,  # The "From" address
                    [recipient_email],  # A list of recipient email addresses
                    fail_silently=False,  # Set to False to raise an exception if sending fails
                )
                return redirect('dashboard/inbox')  # Redirect to inbox after sending email

            except Exception as e:
                print(f"Error sending email: {e}")
                return redirect('dashboard/inbox')


    else:
        initial_data = {
            'sender_email': request.user.email
        }
        form = EmailForm(initial=initial_data)

    context = {
        'form': form
    }

    return render(request, 'dashboard/email_template.html', context)
