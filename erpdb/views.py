from django.shortcuts import render
from .models import Customer, Vendor, Product, SalesOrder, PurchaseOrder, Employee

def dashboard(request):
    context = {
        "customer_count": Customer.objects.count(),
        "vendor_count": Vendor.objects.count(),
        "product_count": Product.objects.count(),
        "sales_order_count": SalesOrder.objects.count(),
        "purchase_order_count": PurchaseOrder.objects.count(),
        "employee_count": Employee.objects.count(),
    }
    #return render(request, "erp/dashboard.html", context)
    return render(request, "dashboard/dashboard.html", context)
