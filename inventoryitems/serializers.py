from rest_framework import serializers
from . import models
from suppliers.serializers import SupplierSerializer


class InventoryItemSerializer(serializers.ModelSerializer):
    suppliers = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = models.InventoryItem
        fields = '__all__'
