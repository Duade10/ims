from django.db import models
from core.models import AbstractTimestamp
from django.utils.text import gettext_lazy as _


class Supplier(AbstractTimestamp):
    """ Inventory Supplier Model Instance """

    name = models.CharField(_("Supplier"), max_length=100)
    contact_information = models.TextField(_("Contact Information"))

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
