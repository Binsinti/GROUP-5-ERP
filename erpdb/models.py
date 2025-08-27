from django.db import models
from django.contrib.auth.models import User

# 1. Customers & Vendors
class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


# 2. Products & Inventory
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)  # simple inventory tracking

    def __str__(self):
        return f"{self.name} ({self.sku})"


# 3. Sales
class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"SO-{self.id} ({self.customer.name})"

class SalesOrderItem(models.Model):
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# 4. Purchases
class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"PO-{self.id} ({self.vendor.name})"

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)


# 5. Accounting (very simple)
class JournalEntry(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Journal {self.id} - {self.date}"

class JournalLine(models.Model):
    journal = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name="lines")
    account_name = models.CharField(max_length=100)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)


# 6. HR
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
