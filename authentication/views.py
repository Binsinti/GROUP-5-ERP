from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.core.mail import send_mail

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'authentication/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request, user)
        return redirect('home')
    return render(request, 'authentication/register.html', {'form': form})


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'authentication/dashboard.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

def finance_view(request):
    return render(request, 'authentication/finance.html')

def home_view(request):
    return render(request, 'authentication/home.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(request, user)
        # Send welcome email
        send_mail(
            'Welcome to Lite WORK ERP',
            'Thank you for registering!',
            None,  # Uses DEFAULT_FROM_EMAIL
            [user.email],
            fail_silently=False,
        )
        return redirect('home')
    return render(request, 'authentication/register.html', {'form': form})


