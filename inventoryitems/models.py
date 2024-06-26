from django.db import models
from django.utils.text import gettext_lazy as _
from core.models import AbstractTimestamp
from django.utils import timezone


class InventoryItem(AbstractTimestamp):
    """ Inventory Item Model Instance """

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    suppliers = models.ManyToManyField("suppliers.Supplier", verbose_name=_("Suppliers"), related_name='items')

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
