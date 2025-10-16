from django.contrib.auth.models import User
from erpdb.models import Customer, Vendor, Product, Category
from django.utils import timezone
import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

def test_auto_codes():
    # Open file to write results
    with open('test_results.txt', 'w') as f:
        f.write("\nTesting Automatic Code Generation...\n")
        f.write(f"Current date: {timezone.now().strftime('%Y-%m-%d')}\n")

        # Create a category first
        electronics_cat, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic products and accessories'}
        )
        f.write(f"\nCreated/Retrieved category: {electronics_cat.name}\n")

        # Get or create a test user
        user, _ = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        f.write(f"Using user: {user.username}\n")

        # Create a test customer
        test_customer = Customer.objects.create(
            name='Test Electronics Inc',
            email=f'contact_{timezone.now().strftime("%Y%m%d")}@testelectronics.com',
            phone='123-456-7890',
            customer_type='business',
            created_by=user
        )
        f.write(f"\nCustomer created:\n")
        f.write(f"Name: {test_customer.name}\n")
        f.write(f"Code: {test_customer.customer_code}\n")
        f.write(f"Expected format: C{timezone.now().strftime('%y%m')}####\n")

        # Create a test vendor
        test_vendor = Vendor.objects.create(
            name='Global Supply Co',
            contact_person='John Smith',
            email=f'john_{timezone.now().strftime("%Y%m%d")}@globalsupply.com',
            phone='987-654-3210',
            vendor_type='supplier',
            created_by=user
        )
        f.write(f"\nVendor created:\n")
        f.write(f"Name: {test_vendor.name}\n")
        f.write(f"Code: {test_vendor.vendor_code}\n")
        f.write(f"Expected format: V{timezone.now().strftime('%y%m')}####\n")

        # Create a test product
        test_product = Product.objects.create(
            name='Test Laptop',
            description='High-performance laptop',
            category=electronics_cat,
            unit_price=999.99,
            cost_price=799.99,
            created_by=user
        )
        f.write(f"\nProduct created:\n")
        f.write(f"Name: {test_product.name}\n")
        f.write(f"SKU: {test_product.sku}\n")
        f.write(f"Expected format: EL{timezone.now().strftime('%y%m')}####\n")

if __name__ == '__main__':
    test_auto_codes()
