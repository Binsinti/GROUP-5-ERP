ProgrammingError at /erp/purchases/
column erpdb_purchaseorder.tax_rate does not exist
LINE 1: ...rder"."status", "erpdb_purchaseorder"."subtotal", "erpdb_pur...
                                                             ^@echo off
echo Clearing Python cache files...

:: Delete all __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

:: Delete all .pyc files
del /s /q *.pyc 2>nul

echo.
echo Cache cleared successfully!
echo.
echo Now testing if forms load correctly...
python -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ERP_PROJECT.settings'); django.setup(); from erpdb.forms import PurchaseOrderForm; print('SUCCESS: Forms loaded without errors')"

echo.
echo Press any key to exit...
pause >nul

