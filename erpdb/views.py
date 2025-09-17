from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.db import models
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.hashers import check_password, make_password
from .models import (
    Customer, Vendor, Category, Product, Warehouse, Inventory,
    SalesOrder, SalesOrderItem, PurchaseOrder, PurchaseOrderItem,
    ChartOfAccounts, JournalEntry, JournalLine,
    Department, Position, Employee, InventoryTransaction, FinancialReport
)
# from .forms import (
#     CustomerForm, VendorForm, ProductForm, SalesOrderForm, PurchaseOrderForm,
#     JournalEntryForm, EmployeeForm, InventoryTransactionForm
# )

# Dashboard Views
@login_required
def dashboard(request):
    # Get current date and date ranges
    today = timezone.now().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    
    # Basic counts
    context = {
        "customer_count": Customer.objects.filter(is_active=True).count(),
        "vendor_count": Vendor.objects.filter(is_active=True).count(),
        "product_count": Product.objects.filter(is_active=True).count(),
        "sales_order_count": SalesOrder.objects.count(),
        "purchase_order_count": PurchaseOrder.objects.count(),
        "employee_count": Employee.objects.filter(employment_status='active').count(),
    }
    
    # Sales analytics
    context.update({
        "total_sales_this_month": SalesOrder.objects.filter(
            order_date__date__gte=this_month_start,
            status__in=['completed', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        
        "total_sales_last_month": SalesOrder.objects.filter(
            order_date__date__gte=last_month_start,
            order_date__date__lte=last_month_end,
            status__in=['completed', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0,
        
        "pending_orders": SalesOrder.objects.filter(status='pending').count(),
        "low_stock_products": Inventory.objects.filter(
            quantity_available__lte=F('reorder_point')
        ).count(),
    })
    
    # Recent activities
    context.update({
        "recent_sales": SalesOrder.objects.select_related('customer').order_by('-order_date')[:5],
        "recent_purchases": PurchaseOrder.objects.select_related('vendor').order_by('-order_date')[:5],
        "low_stock_items": Inventory.objects.select_related('product').filter(
            quantity_available__lte=F('reorder_point')
        )[:5],
    })
    
    return render(request, "erp/dashboard.html", context)

# Settings View
@login_required
def settings(request):
    return render(request, 'erp/settings.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        user = request.user

        if form_type == 'username':
            full_name = request.POST.get('full_name')
            if full_name:
                name_parts = full_name.split(' ', 1)
                user.first_name = name_parts[0]
                user.last_name = name_parts[1] if len(name_parts) > 1 else ''
                user.save()
                messages.success(request, 'Name updated successfully.')

        elif form_type == 'email':
            email = request.POST.get('email')
            if email:
                user.email = email
                user.save()
                messages.success(request, 'Email updated successfully.')

        elif form_type == 'password':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if not check_password(current_password, user.password):
                messages.error(request, 'Current password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            elif len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')

    return redirect('erp:settings')

# Customer Management Views
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customers': page_obj,
        'total_customers': customers.count(),
    }
    return render(request, 'erp/customers/list.html', context)

@login_required
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    sales_orders = SalesOrder.objects.filter(customer=customer).order_by('-order_date')[:10]
    
    context = {
        'customer': customer,
        'sales_orders': sales_orders,
    }
    return render(request, 'erp/customers/detail.html', context)

@login_required
def customer_create(request):
    if request.method == 'POST':
        # Simple form handling for now
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        if name and email:
            customer = Customer.objects.create(
                customer_code=f"CUST-{Customer.objects.count() + 1:04d}",
                name=name,
                email=email,
                phone=phone,
                address=address,
                created_by=request.user
            )
            messages.success(request, 'Customer created successfully.')
            return redirect('erp:customer_detail', customer_id=customer.id)
        else:
            messages.error(request, 'Name and email are required.')
    
    return render(request, 'erp/customers/form.html', {'title': 'Create Customer'})

# Product Management Views
@login_required
def product_list(request):
    products = Product.objects.select_related('category').all().order_by('-created_at')
    category_filter = request.GET.get('category')
    
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': Category.objects.all(),
        'selected_category': category_filter,
    }
    return render(request, 'erp/products/list.html', context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    inventory = Inventory.objects.filter(product=product).select_related('warehouse')
    
    context = {
        'product': product,
        'inventory': inventory,
    }
    return render(request, 'erp/products/detail.html', context)

# Sales Management Views
@login_required
def sales_order_list(request):
    orders = SalesOrder.objects.select_related('customer').all().order_by('-order_date')
    status_filter = request.GET.get('status')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'status_choices': SalesOrder.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'erp/sales/list.html', context)

@login_required
def sales_order_detail(request, order_id):
    order = get_object_or_404(SalesOrder, id=order_id)
    items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'erp/sales/detail.html', context)

# Inventory Management Views
@login_required
def inventory_list(request):
    inventory = Inventory.objects.select_related('product', 'warehouse').all().order_by('product__name')
    warehouse_filter = request.GET.get('warehouse')
    low_stock = request.GET.get('low_stock')
    
    if warehouse_filter:
        inventory = inventory.filter(warehouse_id=warehouse_filter)
    
    if low_stock:
        inventory = inventory.filter(quantity_available__lte=models.F('reorder_point'))
    
    paginator = Paginator(inventory, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inventory': page_obj,
        'warehouses': Warehouse.objects.all(),
        'selected_warehouse': warehouse_filter,
        'low_stock_filter': low_stock,
    }
    return render(request, 'erp/inventory/list.html', context)

# HR Management Views
@login_required
def employee_list(request):
    employees = Employee.objects.select_related('user', 'department', 'position').all().order_by('user__last_name')
    department_filter = request.GET.get('department')
    status_filter = request.GET.get('status')
    
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    
    if status_filter:
        employees = employees.filter(employment_status=status_filter)
    
    paginator = Paginator(employees, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'employees': page_obj,
        'departments': Department.objects.all(),
        'status_choices': Employee.EMPLOYMENT_STATUS_CHOICES,
        'selected_department': department_filter,
        'selected_status': status_filter,
    }
    return render(request, 'erp/hr/employees.html', context)

# Financial Reports Views
@login_required
def financial_reports(request):
    reports = FinancialReport.objects.all().order_by('-generated_at')
    
    context = {
        'reports': reports,
        'report_types': FinancialReport.REPORT_TYPE_CHOICES,
    }
    return render(request, 'erp/finance/reports.html', context)

@login_required
def generate_balance_sheet(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Generate balance sheet logic here
        # This would involve querying ChartOfAccounts and JournalEntry models
        
        messages.success(request, 'Balance sheet generated successfully.')
        return redirect('financial_reports')
    
    return render(request, 'erp/finance/generate_balance_sheet.html')

# Vendor Management Views
@login_required
def vendor_list(request):
    vendors = Vendor.objects.all().order_by('-created_at')
    paginator = Paginator(vendors, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'vendors': page_obj,
        'total_vendors': vendors.count(),
    }
    return render(request, 'erp/vendors/list.html', context)

@login_required
def vendor_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    purchase_orders = PurchaseOrder.objects.filter(vendor=vendor).order_by('-order_date')[:10]
    
    context = {
        'vendor': vendor,
        'purchase_orders': purchase_orders,
    }
    return render(request, 'erp/vendors/detail.html', context)

@login_required
def vendor_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        if name:
            vendor = Vendor.objects.create(
                vendor_code=f"VEND-{Vendor.objects.count() + 1:04d}",
                name=name,
                email=email,
                phone=phone,
                address=address,
                created_by=request.user
            )
            messages.success(request, 'Vendor created successfully.')
            return redirect('erp:vendor_detail', vendor_id=vendor.id)
        else:
            messages.error(request, 'Name is required.')
    
    return render(request, 'erp/vendors/form.html', {'title': 'Create Vendor'})

# Product Management Views
@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sku = request.POST.get('sku')
        unit_price = request.POST.get('unit_price', 0)
        cost_price = request.POST.get('cost_price', 0)
        
        if name and sku:
            product = Product.objects.create(
                name=name,
                sku=sku,
                unit_price=unit_price,
                cost_price=cost_price,
                created_by=request.user
            )
            messages.success(request, 'Product created successfully.')
            return redirect('erp:product_detail', product_id=product.id)
        else:
            messages.error(request, 'Name and SKU are required.')
    
    return render(request, 'erp/products/form.html', {'title': 'Create Product'})

# Sales Management Views
@login_required
def sales_order_create(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        notes = request.POST.get('notes', '')
        
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
                sales_order = SalesOrder.objects.create(
                    order_number=f"SO-{SalesOrder.objects.count() + 1:04d}",
                    customer=customer,
                    notes=notes,
                    created_by=request.user
                )
                messages.success(request, 'Sales order created successfully.')
                return redirect('erp:sales_order_detail', order_id=sales_order.id)
            except Customer.DoesNotExist:
                messages.error(request, 'Customer not found.')
        else:
            messages.error(request, 'Customer is required.')
    
    customers = Customer.objects.all()
    return render(request, 'erp/sales/form.html', {'customers': customers, 'title': 'Create Sales Order'})

# Purchase Management Views
@login_required
def purchase_order_list(request):
    orders = PurchaseOrder.objects.select_related('vendor').all().order_by('-order_date')
    status_filter = request.GET.get('status')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'status_choices': PurchaseOrder.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'erp/purchases/list.html', context)

@login_required
def purchase_order_detail(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)
    items = order.items.select_related('product').all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'erp/purchases/detail.html', context)

@login_required
def purchase_order_create(request):
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor')
        notes = request.POST.get('notes', '')
        
        if vendor_id:
            try:
                vendor = Vendor.objects.get(id=vendor_id)
                purchase_order = PurchaseOrder.objects.create(
                    order_number=f"PO-{PurchaseOrder.objects.count() + 1:04d}",
                    vendor=vendor,
                    notes=notes,
                    created_by=request.user
                )
                messages.success(request, 'Purchase order created successfully.')
                return redirect('erp:purchase_order_detail', order_id=purchase_order.id)
            except Vendor.DoesNotExist:
                messages.error(request, 'Vendor not found.')
        else:
            messages.error(request, 'Vendor is required.')
    
    vendors = Vendor.objects.all()
    return render(request, 'erp/purchases/form.html', {'vendors': vendors, 'title': 'Create Purchase Order'})

# Inventory Management Views
@login_required
def inventory_transaction_list(request):
    transactions = InventoryTransaction.objects.select_related('product', 'warehouse', 'created_by').all().order_by('-created_at')
    
    paginator = Paginator(transactions, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'transactions': page_obj,
    }
    return render(request, 'erp/inventory/transactions.html', context)

@login_required
def inventory_transaction_create(request):
    if request.method == 'POST':
        transaction_type = request.POST.get('transaction_type')
        product_id = request.POST.get('product')
        warehouse_id = request.POST.get('warehouse')
        quantity = request.POST.get('quantity', 0)
        notes = request.POST.get('notes', '')
        
        if transaction_type and product_id and warehouse_id and quantity:
            try:
                product = Product.objects.get(id=product_id)
                warehouse = Warehouse.objects.get(id=warehouse_id)
                transaction = InventoryTransaction.objects.create(
                    transaction_type=transaction_type,
                    product=product,
                    warehouse=warehouse,
                    quantity=int(quantity),
                    notes=notes,
                    created_by=request.user
                )
                messages.success(request, 'Inventory transaction created successfully.')
                return redirect('erp:inventory_transaction_list')
            except (Product.DoesNotExist, Warehouse.DoesNotExist):
                messages.error(request, 'Product or warehouse not found.')
        else:
            messages.error(request, 'All fields are required.')
    
    products = Product.objects.all()
    warehouses = Warehouse.objects.all()
    return render(request, 'erp/inventory/transaction_form.html', {
        'products': products, 
        'warehouses': warehouses, 
        'title': 'Create Inventory Transaction'
    })

# HR Management Views
@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    context = {
        'employee': employee,
    }
    return render(request, 'erp/hr/employee_detail.html', context)

@login_required
def employee_create(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        employee_id = request.POST.get('employee_id')
        salary = request.POST.get('salary', 0)
        hire_date = request.POST.get('hire_date')
        
        if user_id and employee_id and salary and hire_date:
            try:
                user = User.objects.get(id=user_id)
                employee = Employee.objects.create(
                    user=user,
                    employee_id=employee_id,
                    salary=salary,
                    hire_date=hire_date
                )
                messages.success(request, 'Employee created successfully.')
                return redirect('erp:employee_detail', employee_id=employee.id)
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'All fields are required.')
    
    users = User.objects.all()
    return render(request, 'erp/hr/employee_form.html', {'users': users, 'title': 'Create Employee'})

# API Views for AJAX requests
@login_required
def get_customer_data(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    data = {
        'id': str(customer.id),
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone,
        'address': customer.address,
        'credit_limit': float(customer.credit_limit),
    }
    return JsonResponse(data)

@login_required
def get_product_data(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'id': str(product.id),
        'name': product.name,
        'sku': product.sku,
        'unit_price': float(product.unit_price),
        'cost_price': float(product.cost_price),
        'available_quantity': Inventory.objects.filter(product=product).aggregate(
            total=Sum('quantity_available')
        )['total'] or 0,
    }
    return JsonResponse(data)
