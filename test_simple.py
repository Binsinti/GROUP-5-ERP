import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

from django.contrib.auth.models import User
from erpdb.models import Customer, Vendor, Product, Category
from django.utils import timezone

print("Testing code generation...")

# Get or create test user
user = User.objects.filter(username='test_user').first()
if not user:
    user = User.objects.create_user('test_user', 'test@example.com', 'password')

# Create test category
category = Category.objects.create(name='Electronics')

# Test customer code generation
customer = Customer.objects.create(
    name='Test Customer',
    email='test@customer.com',
    customer_type='business',
    created_by=user
)
print(f"Generated customer code: {customer.customer_code}")

# Test vendor code generation
vendor = Vendor.objects.create(
    name='Test Vendor',
    email='test@vendor.com',
    vendor_type='supplier',
    created_by=user
)
print(f"Generated vendor code: {vendor.vendor_code}")

# Test product SKU generation
product = Product.objects.create(
    name='Test Product',
    category=category,
    unit_price=100.00,
    cost_price=80.00,
    created_by=user
)
print(f"Generated product SKU: {product.sku}")

print("Code generation test completed.")
