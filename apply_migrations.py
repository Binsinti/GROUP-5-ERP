import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings')
django.setup()

from django.core.management import call_command

print("=" * 60)
print("Applying pending migrations...")
print("=" * 60)

try:
    # Show current migration status
    print("\nCurrent migration status:")
    call_command('showmigrations', 'erpdb')

    print("\n" + "=" * 60)
    print("Applying migrations...")
    print("=" * 60)

    # Apply migrations
    call_command('migrate', 'erpdb', verbosity=2)

    print("\n" + "=" * 60)
    print("✓ Migrations applied successfully!")
    print("=" * 60)

    # Show updated migration status
    print("\nUpdated migration status:")
    call_command('showmigrations', 'erpdb')

except Exception as e:
    print(f"\n✗ Error applying migrations: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

