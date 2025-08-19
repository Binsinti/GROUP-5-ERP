from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('finance/', views.finance_view, name='finance'),

    path('inbox/', views.inbox_view, name='inbox'),
    path('products/', views.products_view, name='products'),
]
