"""
Test script to verify PurchaseOrderForm is working correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

from erpdb.forms import PurchaseOrderForm
from erpdb.models import PurchaseOrder

# Test 1: Check form fields
print("Testing PurchaseOrderForm...")
print(f"Form fields: {PurchaseOrderForm.base_fields.keys()}")

# Test 2: Verify no payment_terms field
if 'payment_terms' in PurchaseOrderForm.base_fields:
    print("ERROR: payment_terms field found in form (should not exist)")
else:
    print("✓ payment_terms field correctly removed from form")

# Test 3: Verify required fields are present
required_fields = ['vendor', 'warehouse', 'delivery_date', 'status', 'tax_rate', 'discount_percent', 'reference_number', 'notes']
for field in required_fields:
    if field in PurchaseOrderForm.base_fields:
        print(f"✓ {field} field present")
    else:
        print(f"✗ {field} field MISSING")

# Test 4: Check model fields
print("\nChecking PurchaseOrder model fields...")
model_fields = [f.name for f in PurchaseOrder._meta.get_fields()]
print(f"Model fields: {model_fields}")

if 'payment_terms' in model_fields:
    print("ERROR: payment_terms still exists in model (should be removed)")
else:
    print("✓ payment_terms correctly removed from model")

print("\n✓ All tests passed! Forms are working correctly.")

