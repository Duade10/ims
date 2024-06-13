from django.contrib import admin

from . import models


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name"]