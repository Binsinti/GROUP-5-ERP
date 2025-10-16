from django.shortcuts import render
from erpdb.models import Customer, Vendor, Product, Category
from django.utils import timezone

def test_code_generation(request):
    """View to test auto-generated codes"""
    # Create a category first
    electronics_cat, _ = Category.objects.get_or_create(
        name='Electronics',
        defaults={'description': 'Electronic products and accessories'}
    )

    # Create test entries with timestamp to ensure uniqueness
    timestamp = timezone.now().timestamp()

    # Create a test customer
    customer = Customer.objects.create(
        name=f'Test Customer {timestamp}',
        email=f'customer_{timestamp}@test.com',
        customer_type='business'
    )

    # Create a test vendor
    vendor = Vendor.objects.create(
        name=f'Test Vendor {timestamp}',
        email=f'vendor_{timestamp}@test.com',
        vendor_type='supplier'
    )

    # Create a test product
    product = Product.objects.create(
        name=f'Test Product {timestamp}',
        category=electronics_cat,
        unit_price=100.00,
        cost_price=80.00
    )

    context = {
        'customer': customer,
        'vendor': vendor,
        'product': product,
        'current_date': timezone.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'erp/test_codes.html', context)
