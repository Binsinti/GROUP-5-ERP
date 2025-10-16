from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erpdb.models import Customer, Vendor, Product, Category
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create test records with automatic code generation'

    def handle(self, *args, **options):
        # Create test user if not exists
        user, _ = User.objects.get_or_create(
            username='testadmin',
            defaults={'is_staff': True, 'is_superuser': True}
        )

        # Create category
        electronics_cat, created = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic products and accessories'}
        )
        self.stdout.write(f'Category {"created" if created else "exists"}: Electronics')

        # Create customer
        customer = Customer.objects.create(
            name='Test Electronics Inc',
            email=f'contact_{timezone.now().timestamp()}@testelectronics.com',
            phone='123-456-7890',
            customer_type='business',
            created_by=user
        )
        self.stdout.write(f'Created customer with code: {customer.customer_code}')

        # Create vendor
        vendor = Vendor.objects.create(
            name='Global Supply Co',
            contact_person='John Smith',
            email=f'john_{timezone.now().timestamp()}@globalsupply.com',
            phone='987-654-3210',
            vendor_type='supplier',
            created_by=user
        )
        self.stdout.write(f'Created vendor with code: {vendor.vendor_code}')

        # Create product
        product = Product.objects.create(
            name='Test Laptop',
            description='High-performance laptop',
            category=electronics_cat,
            unit_price=999.99,
            cost_price=799.99,
            created_by=user
        )
        self.stdout.write(f'Created product with SKU: {product.sku}')
