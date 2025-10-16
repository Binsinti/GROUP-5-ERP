#!/usr/bin/env python
"""
Script to fix the invoice creation for purchase orders in populate_sample_data script.
"""
import os
import re

def fix_invoice_creation_script():
    # Set path to populate_sample_data.py
    script_path = os.path.join('erpdb', 'management', 'commands', 'populate_sample_data.py')
    
    # Read the file content
    with open(script_path, 'r') as file:
        content = file.read()
    
    # Replace order.order_number with order.po_number for purchase orders
    fixed_content = content.replace(
        "notes=f'Invoice for purchase order {order.order_number}',", 
        "notes=f'Invoice for purchase order {order.po_number}',"
    )
    
    # Write the fixed content back to the file
    with open(script_path, 'w') as file:
        file.write(fixed_content)
    
    print(f"✓ Fixed invoice creation for purchase orders in {script_path}")

if __name__ == "__main__":
    fix_invoice_creation_script()
