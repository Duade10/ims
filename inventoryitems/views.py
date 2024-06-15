from rest_framework import viewsets
from . import models
from .serializers import InventoryItemSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = models.InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
