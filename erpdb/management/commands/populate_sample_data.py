from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from erpdb.models import (
    Customer, Vendor, Category, Product, Warehouse, Inventory,
    Department, Position, Employee, ChartOfAccounts
)

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user (admin/admin123)')
        
        # Create categories
        electronics, _ = Category.objects.get_or_create(
            name='Electronics',
            defaults={'description': 'Electronic products and gadgets'}
        )
        
        clothing, _ = Category.objects.get_or_create(
            name='Clothing',
            defaults={'description': 'Apparel and fashion items'}
        )
        
        # Create warehouses
        main_warehouse, _ = Warehouse.objects.get_or_create(
            name='Main Warehouse',
            defaults={
                'address': '123 Main St, City, State',
                'is_active': True
            }
        )
        
        # Create customers
        customers_data = [
            {'name': 'Acme Corporation', 'email': 'contact@acme.com', 'customer_type': 'business'},
            {'name': 'John Smith', 'email': 'john@example.com', 'customer_type': 'individual'},
            {'name': 'Tech Solutions Inc', 'email': 'info@techsolutions.com', 'customer_type': 'business'},
        ]
        
        for i, data in enumerate(customers_data, 1):
            customer, created = Customer.objects.get_or_create(
                email=data['email'],
                defaults={
                    'customer_code': f'CUST-{i:04d}',
                    'name': data['name'],
                    'customer_type': data['customer_type'],
                    'phone': '+1-555-0123',
                    'address': '123 Business St, City, State 12345',
                    'credit_limit': 10000.00,
                    'created_by': User.objects.first()
                }
            )
            if created:
                self.stdout.write(f'Created customer: {customer.name}')
        
        # Create vendors
        vendors_data = [
            {'name': 'Global Suppliers Ltd', 'email': 'orders@globalsuppliers.com'},
            {'name': 'Tech Distributors Inc', 'email': 'sales@techdist.com'},
            {'name': 'Fashion Wholesale Co', 'email': 'wholesale@fashionco.com'},
        ]
        
        for i, data in enumerate(vendors_data, 1):
            vendor, created = Vendor.objects.get_or_create(
                email=data['email'],
                defaults={
                    'vendor_code': f'VEND-{i:04d}',
                    'name': data['name'],
                    'contact_person': 'Sales Manager',
                    'phone': '+1-555-0456',
                    'address': '456 Supplier Ave, City, State 12345',
                    'vendor_type': 'supplier',
                    'created_by': User.objects.first()
                }
            )
            if created:
                self.stdout.write(f'Created vendor: {vendor.name}')
        
        # Create products
        products_data = [
            {'name': 'Laptop Computer', 'sku': 'LAPTOP-001', 'category': electronics, 'unit_price': 999.99, 'cost_price': 750.00},
            {'name': 'Smartphone', 'sku': 'PHONE-001', 'category': electronics, 'unit_price': 699.99, 'cost_price': 500.00},
            {'name': 'T-Shirt', 'sku': 'TSHIRT-001', 'category': clothing, 'unit_price': 29.99, 'cost_price': 15.00},
            {'name': 'Jeans', 'sku': 'JEANS-001', 'category': clothing, 'unit_price': 79.99, 'cost_price': 40.00},
        ]
        
        for data in products_data:
            product, created = Product.objects.get_or_create(
                sku=data['sku'],
                defaults={
                    'name': data['name'],
                    'category': data['category'],
                    'unit_price': data['unit_price'],
                    'cost_price': data['cost_price'],
                    'description': f'High-quality {data["name"].lower()}',
                    'product_type': 'product',
                    'unit_of_measure': 'each',
                    'is_active': True,
                    'created_by': User.objects.first()
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
                
                # Create inventory for the product
                Inventory.objects.create(
                    product=product,
                    warehouse=main_warehouse,
                    quantity_on_hand=100,
                    quantity_reserved=0,
                    quantity_available=100,
                    reorder_point=10,
                    reorder_quantity=50
                )
        
        # Create departments
        departments_data = [
            {'name': 'Sales', 'description': 'Sales and marketing department'},
            {'name': 'IT', 'description': 'Information technology department'},
            {'name': 'HR', 'description': 'Human resources department'},
        ]
        
        for data in departments_data:
            dept, created = Department.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create positions
        positions_data = [
            {'title': 'Sales Manager', 'department': Department.objects.get(name='Sales'), 'min_salary': 50000, 'max_salary': 80000},
            {'title': 'Software Developer', 'department': Department.objects.get(name='IT'), 'min_salary': 60000, 'max_salary': 100000},
            {'title': 'HR Specialist', 'department': Department.objects.get(name='HR'), 'min_salary': 45000, 'max_salary': 65000},
        ]
        
        for data in positions_data:
            position, created = Position.objects.get_or_create(
                title=data['title'],
                defaults={
                    'department': data['department'],
                    'description': f'Position for {data["title"]}',
                    'min_salary': data['min_salary'],
                    'max_salary': data['max_salary']
                }
            )
            if created:
                self.stdout.write(f'Created position: {position.title}')
        
        # Create chart of accounts
        accounts_data = [
            {'account_code': '1000', 'account_name': 'Assets', 'account_type': 'asset', 'is_active': True},
            {'account_code': '1100', 'account_name': 'Cash', 'account_type': 'asset', 'parent_account': '1000', 'is_active': True},
            {'account_code': '2000', 'account_name': 'Liabilities', 'account_type': 'liability', 'is_active': True},
            {'account_code': '3000', 'account_name': 'Equity', 'account_type': 'equity', 'is_active': True},
            {'account_code': '4000', 'account_name': 'Revenue', 'account_type': 'revenue', 'is_active': True},
            {'account_code': '5000', 'account_name': 'Expenses', 'account_type': 'expense', 'is_active': True},
        ]
        
        for data in accounts_data:
            account, created = ChartOfAccounts.objects.get_or_create(
                account_code=data['account_code'],
                defaults={
                    'account_name': data['account_name'],
                    'account_type': data['account_type'],
                    'is_active': data['is_active']
                }
            )
            if created:
                self.stdout.write(f'Created account: {account.account_name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
        self.stdout.write('You can now login with admin/admin123 to test the system.')
