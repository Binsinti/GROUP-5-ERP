from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erpdb.models import Customer, Vendor, Product, Category

class Command(BaseCommand):
    help = 'Create test records to demonstrate automatic code generation'

    def handle(self, *args, **options):
        # Create a category first
        electronics_cat, created = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic products and accessories'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Electronics category'))

        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={'email': 'test@example.com'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create a test customer
        customer = Customer.objects.create(
            name='Test Electronics Inc',
            email='contact@testelectronics.com',
            phone='123-456-7890',
            customer_type='business',
            created_by=user
        )
        self.stdout.write(self.style.SUCCESS(f'Created customer with code: {customer.customer_code}'))

        # Create a test vendor
        vendor = Vendor.objects.create(
            name='Global Supply Co',
            contact_person='John Smith',
            email='john@globalsupply.com',
            phone='987-654-3210',
            vendor_type='supplier',
            created_by=user
        )
        self.stdout.write(self.style.SUCCESS(f'Created vendor with code: {vendor.vendor_code}'))

        # Create a test product
        product = Product.objects.create(
            name='Test Laptop',
            description='High-performance laptop',
            category=electronics_cat,
            unit_price=999.99,
            cost_price=799.99,
            created_by=user
        )
        self.stdout.write(self.style.SUCCESS(f'Created product with SKU: {product.sku}'))
