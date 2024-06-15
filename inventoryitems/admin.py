from django.contrib import admin

from . import models


@admin.register(models.InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "date_added"]
