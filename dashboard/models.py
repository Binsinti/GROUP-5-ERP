from django.db import models

# Create your models here.
class Email(models.Model):
    sender_email = models.EmailField(unique=True)
    recipient_email = models.EmailField(unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sender_email
