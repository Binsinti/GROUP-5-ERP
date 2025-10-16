#!/usr/bin/env python
"""
Script to directly fix missing receipt columns in the payment table.
This script will run the necessary ALTER TABLE commands to add the missing columns.
"""
import os
import sys
import django
from django.db import connection

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

def add_missing_columns():
    """Add the missing receipt columns to the payment table"""
    results = []

    with connection.cursor() as cursor:
        # Check if the receipt_generated column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='erpdb_payment' AND column_name='receipt_generated'
        """)
        receipt_generated_exists = bool(cursor.fetchone())

        # Check if the receipt_number column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='erpdb_payment' AND column_name='receipt_number'
        """)
        receipt_number_exists = bool(cursor.fetchone())

        # Add the missing columns if they don't exist
        if not receipt_generated_exists:
            results.append("Adding receipt_generated column...")
            try:
                cursor.execute("ALTER TABLE erpdb_payment ADD COLUMN receipt_generated BOOLEAN DEFAULT FALSE")
                results.append("✅ receipt_generated column added successfully")
            except Exception as e:
                results.append(f"❌ Error adding receipt_generated column: {str(e)}")
        else:
            results.append("⚠️ receipt_generated column already exists, skipping")

        if not receipt_number_exists:
            results.append("Adding receipt_number column...")
            try:
                cursor.execute("ALTER TABLE erpdb_payment ADD COLUMN receipt_number VARCHAR(20) NULL")
                results.append("✅ receipt_number column added successfully")
            except Exception as e:
                results.append(f"❌ Error adding receipt_number column: {str(e)}")
        else:
            results.append("⚠️ receipt_number column already exists, skipping")

    return results

if __name__ == "__main__":
    results = ["Starting database fix..."]
    results.extend(add_missing_columns())
    results.append("Fix complete. You can now restart your Django server and the payments page should work!")

    # Print to console
    for line in results:
        print(line)

    # Also write to a file
    with open('fix_payment_columns_results.txt', 'w') as f:
        for line in results:
            f.write(line + '\n')
