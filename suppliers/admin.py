from django.contrib import admin

from . import models


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "total_items"]

    def total_items(self, obj):
        return obj.items.count()

    total_items.short_description = "No of Items"
