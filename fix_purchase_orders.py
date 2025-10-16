#!/usr/bin/env python
"""
Script to fix the PurchaseOrder creation in populate_sample_data script
and run the sample data population.
"""
import os
import sys
import re

def fix_purchase_orders_script():
    # Set path to populate_sample_data.py
    script_path = os.path.join('erpdb', 'management', 'commands', 'populate_sample_data.py')
    
    # Read the file content
    with open(script_path, 'r') as file:
        content = file.read()
    
    # Define the correct replacement function
    correct_function = '''
    def _create_purchase_orders(self, created_by, vendors, products):
        # Clear existing purchase orders
        PurchaseOrder.objects.all().delete()

        # Get first warehouse for purchase orders
        warehouses = Warehouse.objects.all()
        if not warehouses.exists():
            self.stdout.write(self.style.WARNING('No warehouses found, skipping purchase orders'))
            return []

        # Create 8 purchase orders with random items
        purchase_orders = []
        for i in range(1, 9):
            # Pick a random vendor
            vendor = random.choice(vendors)
            warehouse = random.choice(warehouses)

            # Create an order with a recent date
            days_ago = random.randint(1, 60)
            order_date = timezone.now() - timedelta(days=days_ago)

            # Random status - fix the status choices to match model
            status_choices = ['draft', 'pending', 'confirmed', 'received', 'completed']
            status_weights = [0.1, 0.2, 0.3, 0.2, 0.2]
            status = random.choices(status_choices, weights=status_weights, k=1)[0]

            # Create the order
            order = PurchaseOrder.objects.create(
                po_number=f'PO{i:06d}',
                vendor=vendor,
                warehouse=warehouse,
                status=status,
                notes=f'Sample purchase order {i}',
                created_by=created_by
            )

            # Add 1-5 random products to the order
            num_items = random.randint(1, 5)

            for _ in range(num_items):
                # Pick a random product (excluding services for simplicity)
                product = random.choice([p for p in products if p.product_type != 'service'])

                # Random quantity
                quantity = random.randint(5, 50)

                # Add the item - use correct field name unit_price
                PurchaseOrderItem.objects.create(
                    purchase_order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=product.cost_price
                )

            # Calculate totals using model method
            order.calculate_totals()

            purchase_orders.append(order)

        return purchase_orders'''
    
    # Find the existing _create_purchase_orders function and replace it
    pattern = r'def _create_purchase_orders\(self, created_by, vendors, products\):.*?return purchase_orders'
    replacement = correct_function.strip()
    
    # Use regex with DOTALL flag to match across multiple lines
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the fixed content back to the file
    with open(script_path, 'w') as file:
        file.write(new_content)
    
    print(f"✓ Fixed PurchaseOrder creation in {script_path}")

if __name__ == "__main__":
    fix_purchase_orders_script()
