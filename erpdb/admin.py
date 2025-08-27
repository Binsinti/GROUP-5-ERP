from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(SalesOrder)
admin.site.register(SalesOrderItem)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(JournalEntry)
admin.site.register(JournalLine)
admin.site.register(Employee)
