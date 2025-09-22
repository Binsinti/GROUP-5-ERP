from django.contrib import admin
from django.urls import path
from Email.views import email_view

# Remove this line:
# app_name = 'Email'

urlpatterns = [
    path('compose/', email_view, name="email_view"),
]