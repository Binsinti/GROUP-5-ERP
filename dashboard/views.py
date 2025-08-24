from django.shortcuts import render, redirect

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
    return render(request, 'dashboard/inbox.html')

def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/settings.html')

def navbar_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/navbar.html')





