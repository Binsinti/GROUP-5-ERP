import os
import django
import sys
from datetime import datetime

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

from django.contrib.auth.models import User
from erpdb.models import Vendor

def test_vendor_creation():
    # Create test user if doesn't exist
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )

    results = []
    results.append("=== Vendor Code Generation Test ===")
    results.append(f"Test run at: {datetime.now()}")
    results.append("")

    try:
        # Create first vendor
        vendor1 = Vendor.objects.create(
            name='Test Vendor 1',
            email='vendor1@test.com',
            phone='123-456-7890',
            created_by=user
        )
        results.append(f"Created Vendor 1: {vendor1.name}")
        results.append(f"Vendor Code 1: {vendor1.vendor_code}")

        # Create second vendor
        vendor2 = Vendor.objects.create(
            name='Test Vendor 2',
            email='vendor2@test.com',
            phone='123-456-7891',
            created_by=user
        )
        results.append(f"Created Vendor 2: {vendor2.name}")
        results.append(f"Vendor Code 2: {vendor2.vendor_code}")

        results.append("")
        results.append("Test completed successfully!")

    except Exception as e:
        results.append(f"Error occurred: {str(e)}")

    # Clean up test data
    Vendor.objects.filter(email__in=['vendor1@test.com', 'vendor2@test.com']).delete()

    return "\n".join(results)

if __name__ == '__main__':
    # Run the test and write results to file
    test_results = test_vendor_creation()
    with open('test_results.txt', 'w') as f:
        f.write(test_results)
