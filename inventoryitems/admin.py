from django.contrib import admin

from . import models


@admin.register(models.InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "total_suppliers", "created_at"]

    def total_suppliers(self, obj):
        return obj.suppliers.count()

    total_suppliers.short_description = "No of Suppliers"
