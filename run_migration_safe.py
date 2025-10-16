import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

from django.core.management import call_command
from django.db import connection

print("=" * 70)
print("CHECKING DATABASE STATE")
print("=" * 70)

# Check current columns in purchaseorder table
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='erpdb_purchaseorder'
        ORDER BY ordinal_position
    """)
    columns = [row[0] for row in cursor.fetchall()]
    print("\nCurrent columns in erpdb_purchaseorder:")
    for col in columns:
        print(f"  - {col}")

    if 'payment_terms' in columns:
        print("\n⚠ payment_terms column EXISTS (will be removed)")
    else:
        print("\n✓ payment_terms column does NOT exist (safe to proceed)")

    if 'tax_rate' in columns:
        print("✓ tax_rate column EXISTS")
    else:
        print("⚠ tax_rate column MISSING (will be added)")

print("\n" + "=" * 70)
print("APPLYING MIGRATION 0009")
print("=" * 70)

try:
    call_command('migrate', 'erpdb', '0009', verbosity=2)
    print("\n" + "=" * 70)
    print("✓ MIGRATION SUCCESSFUL!")
    print("=" * 70)
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Verify the changes
print("\n" + "=" * 70)
print("VERIFYING CHANGES")
print("=" * 70)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='erpdb_purchaseorder'
        ORDER BY ordinal_position
    """)
    columns_after = [row[0] for row in cursor.fetchall()]
    print("\nColumns in erpdb_purchaseorder after migration:")
    for col in columns_after:
        print(f"  - {col}")

# Check for required fields
required_fields = ['tax_rate', 'discount_percent', 'discount_amount', 'paid_amount']
missing_fields = [f for f in required_fields if f not in columns_after]

if missing_fields:
    print(f"\n✗ MISSING FIELDS: {missing_fields}")
    sys.exit(1)
else:
    print(f"\n✓ All required fields present: {required_fields}")

if 'payment_terms' in columns_after:
    print("⚠ WARNING: payment_terms still exists")
else:
    print("✓ payment_terms successfully removed")

print("\n" + "=" * 70)
print("✓ DATABASE MIGRATION COMPLETE!")
print("=" * 70)

