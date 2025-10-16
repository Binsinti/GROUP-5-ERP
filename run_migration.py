import os
import django
import sys
from io import StringIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

from django.core.management import call_command

# Redirect output to capture it
output = StringIO()

print("Checking migration status...")
call_command('showmigrations', 'erpdb', stdout=output)
status_before = output.getvalue()

print("Migration status BEFORE:")
print(status_before)

# Apply migrations
output = StringIO()
print("\nApplying migrations...")
try:
    call_command('migrate', 'erpdb', verbosity=2, stdout=output)
    migration_result = output.getvalue()
    print(migration_result)
    print("\n✓ SUCCESS: Migrations applied!")
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Check status after
output = StringIO()
call_command('showmigrations', 'erpdb', stdout=output)
status_after = output.getvalue()

print("\nMigration status AFTER:")
print(status_after)

with open('migration_results.txt', 'w') as f:
    f.write("BEFORE:\n")
    f.write(status_before)
    f.write("\n\nRESULT:\n")
    f.write(migration_result if 'migration_result' in locals() else "Failed")
    f.write("\n\nAFTER:\n")
    f.write(status_after)

print("\n✓ Results saved to migration_results.txt")

