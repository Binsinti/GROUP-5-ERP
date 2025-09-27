import os

from django.db import models
import random
# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    new_filename = random.randint(1, 10000)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "MONA/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

class Email(models.Model):
    sender_email = models.EmailField(unique=True)
    recipient_email = models.EmailField(unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)


    def __str__(self):
        return self.sender_email
