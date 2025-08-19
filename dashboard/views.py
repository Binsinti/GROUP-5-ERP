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

def inbox_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard/inbox.html')




