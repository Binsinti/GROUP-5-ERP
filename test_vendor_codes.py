from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from erpdb.models import Vendor
import datetime

class VendorCodeGenerationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_vendor_code_generation(self):
        # Create first vendor
        vendor1 = Vendor.objects.create(
            name='Test Vendor 1',
            email='vendor1@test.com',
            phone='123-456-7890',
            created_by=self.user
        )

        # Create second vendor
        vendor2 = Vendor.objects.create(
            name='Test Vendor 2',
            email='vendor2@test.com',
            phone='123-456-7891',
            created_by=self.user
        )

        # Get current year and month
        year = timezone.now().strftime('%y')
        month = timezone.now().strftime('%m')

        # Expected format is VYYMM####
        expected_prefix = f'V{year}{month}'

        # Check if vendor codes are generated correctly
        self.assertTrue(vendor1.vendor_code.startswith(expected_prefix))
        self.assertTrue(vendor2.vendor_code.startswith(expected_prefix))

        # Check if sequence numbers are correct
        seq1 = int(vendor1.vendor_code[-4:])
        seq2 = int(vendor2.vendor_code[-4:])
        self.assertEqual(seq1, 1)  # First vendor should be 0001
        self.assertEqual(seq2, 2)  # Second vendor should be 0002

        # Check total length
        self.assertEqual(len(vendor1.vendor_code), 8)  # VYYMM#### = 8 characters
        self.assertEqual(len(vendor2.vendor_code), 8)

        return {
            'vendor1_code': vendor1.vendor_code,
            'vendor2_code': vendor2.vendor_code
        }
