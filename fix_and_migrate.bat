@echo off
echo ========================================
echo FIXING MIGRATION AND APPLYING CHANGES
echo ========================================
echo.

cd C:\Users\Vince\GROUP-5-ERP

echo Step 1: Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo Cache cleared.
echo.

echo Step 2: Creating new migration for payment_due_date field...
python manage.py makemigrations erpdb
echo.

echo Step 3: Checking migration status...
python manage.py showmigrations erpdb
echo.

echo Step 4: Applying migration 0009 (with fixed payment_terms removal)...
python manage.py migrate erpdb 0009
echo.

echo Step 5: Applying all remaining migrations...
python manage.py migrate erpdb
echo.

echo Step 6: Verifying database schema...
python -c "import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings'); django.setup(); from django.db import connection; cursor = connection.cursor(); cursor.execute(\"SELECT column_name FROM information_schema.columns WHERE table_name='erpdb_purchaseorder' ORDER BY column_name\"); cols = [r[0] for r in cursor.fetchall()]; print('Columns in erpdb_purchaseorder:'); [print(f'  - {c}') for c in cols]; print(); print('Required fields check:'); print(f\"  tax_rate: {'YES' if 'tax_rate' in cols else 'MISSING'}\"); print(f\"  discount_percent: {'YES' if 'discount_percent' in cols else 'MISSING'}\"); print(f\"  discount_amount: {'YES' if 'discount_amount' in cols else 'MISSING'}\"); print(f\"  paid_amount: {'YES' if 'paid_amount' in cols else 'MISSING'}\"); print(f\"  payment_due_date: {'YES' if 'payment_due_date' in cols else 'MISSING'}\"); print(f\"  payment_terms: {'STILL EXISTS (ERROR)' if 'payment_terms' in cols else 'Removed (OK)'}\")"
echo.

echo ========================================
echo Migration Complete!
echo ========================================
echo.
echo Purchase Order form has been updated with:
echo   - Tax Rate field
echo   - Discount Percent field
echo   - Payment Due Date field (replacing Payment Terms)
echo   - Modern UI matching Sales Order design
echo.
echo You can now restart your Django server.
echo.
pause
