from django.urls import path
from . import views

app_name = 'erp'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Settings
    path('settings/', views.settings, name='settings'),
    path('update-profile/', views.update_profile, name='update_profile'),

    # Customer Management
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<uuid:customer_id>/', views.customer_detail, name='customer_detail'),
    
    # Vendor Management
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.vendor_create, name='vendor_create'),
    path('vendors/<uuid:vendor_id>/', views.vendor_detail, name='vendor_detail'),
    
    # Product Management
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<uuid:product_id>/', views.product_detail, name='product_detail'),
    
    # Sales Management
    path('sales/', views.sales_order_list, name='sales_order_list'),
    path('sales/create/', views.sales_order_create, name='sales_order_create'),
    path('sales/<uuid:order_id>/', views.sales_order_detail, name='sales_order_detail'),
    
    # Purchase Management
    path('purchases/', views.purchase_order_list, name='purchase_order_list'),
    path('purchases/create/', views.purchase_order_create, name='purchase_order_create'),
    path('purchases/<uuid:order_id>/', views.purchase_order_detail, name='purchase_order_detail'),
    
    # Inventory Management
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/transactions/', views.inventory_transaction_list, name='inventory_transaction_list'),
    path('inventory/transactions/create/', views.inventory_transaction_create, name='inventory_transaction_create'),
    
    # HR Management
    path('hr/employees/', views.employee_list, name='employee_list'),
    path('hr/employees/create/', views.employee_create, name='employee_create'),
    path('hr/employees/<uuid:employee_id>/', views.employee_detail, name='employee_detail'),
    
    # Financial Reports
    path('reports/', views.financial_reports, name='financial_reports'),
    path('reports/balance-sheet/', views.generate_balance_sheet, name='generate_balance_sheet'),
    
    # API Endpoints
    path('api/customer/<uuid:customer_id>/', views.get_customer_data, name='api_customer_data'),
    path('api/product/<uuid:product_id>/', views.get_product_data, name='api_product_data'),
]
