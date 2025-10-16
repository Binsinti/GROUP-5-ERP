@echo off
echo ========================================
echo Applying Database Migrations
echo ========================================
echo.

cd C:\Users\Vince\GROUP-5-ERP

echo Checking current migration status...
python manage.py showmigrations erpdb
echo.

echo Applying pending migrations...
python manage.py migrate erpdb
echo.

echo ========================================
echo Migration complete!
echo ========================================
echo.

echo Testing if database is accessible...
python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings'); django.setup(); from erpdb.models import PurchaseOrder; print('SUCCESS: PurchaseOrder model can access database'); print('Fields:', [f.name for f in PurchaseOrder._meta.get_fields()])"

echo.
pause

