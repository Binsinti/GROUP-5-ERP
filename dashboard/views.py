from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
import imaplib
import email
from email.header import decode_header
import ssl
from django.conf import settings
from datetime import datetime

# Create your views here.

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/dashboard.html')

def finance_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/finance.html')

def clients_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/clients.html')

def products_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/products.html')

def activity_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/activity.html')
def inbox_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

        # Handle email form submission
    if request.method == 'POST':
        # Check if this is an email compose form submission
        if 'to_email' in request.POST:
            to_email = request.POST.get('to_email')
            cc_email = request.POST.get('cc_email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            attachment = request.FILES.get('attachment')

            try:
                # Create email
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[to_email],
                )

                # Add CC if provided
                if cc_email:
                    email.cc = [cc_email]

                # Add attachment if provided
                if attachment:
                    email.attach(attachment.name, attachment.read(), attachment.content_type)

                # Send email
                email.send()
                messages.success(request, 'Email sent successfully!')

            except Exception as e:
                messages.error(request, f'Failed to send email: {str(e)}')

            # Redirect to prevent re-submission on refresh
            return redirect('inbox')

    print("Fetching emails...")
    received_emails = fetch_emails()
    print(f"Found {len(received_emails)} emails")

    for email in received_emails:
        print(f"Email: {email['subject']} from {email['from']}")
        print(f"Email data: {email}")  # Add this line to see full email data

    context = {
        'emails': received_emails
    }

    return render(request, 'dashboard/inbox.html', context)

def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/settings.html')

def navbar_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/navbar.html')


def fetch_emails():
    """Fetch emails from Gmail IMAP"""
    try:
        import imaplib
        import email
        from email.header import decode_header
        import ssl
        from django.conf import settings
        import html

        # Connect to Gmail IMAP server
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993, ssl_context=context)
        mail.login('wlite0990@gmail.com', 'fvlwllnqfemtadap')

        # Select inbox
        mail.select("inbox")

        # Search for all emails
        status, messages = mail.search(None, "ALL")

        emails = []
        email_ids = messages[0].split()

        # Fetch last 10 emails
        for email_id in email_ids[-10:]:
            try:
                status, msg_data = mail.fetch(email_id, "(RFC822)")

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Decode subject
                        subject = msg.get("Subject", "No Subject")
                        if subject:
                            decoded_subject = decode_header(subject)[0][0]
                            if isinstance(decoded_subject, bytes):
                                subject = decoded_subject.decode()

                        # Get sender
                        from_email = msg.get("From", "Unknown Sender")

                        # Get date
                        date_str = msg.get("Date", "No Date")

                        # Get body
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    try:
                                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                        break
                                    except:
                                        body = "Could not decode message content"
                        else:
                            try:
                                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                            except:
                                body = "Could not decode message content"
                        body = html.unescape(body)
                        body = body.replace('\r\n', '\n').replace('\r', '\n')

                        emails.append({
                            'id': email_id.decode() if isinstance(email_id, bytes) else str(email_id),
                            'subject': subject,
                            'from': from_email,
                            'date': date_str,
                            'body': body[:200] + "..." if len(body) > 200 else body,
                            'full_body': body
                        })
            except Exception as e:
                print(f"Error processing email {email_id}: {e}")
                continue

        mail.close()
        mail.logout()

        return emails

    except Exception as e:
        print(f"Error fetching emails: {e}")
        return []




