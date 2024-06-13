from django.db import models
from django.utils.text import gettext_lazy as _


class AbstractTimestamp(models.Model):
    """Abstract model to add to other models"""

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True
