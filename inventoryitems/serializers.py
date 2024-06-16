from rest_framework import serializers

from suppliers.models import Supplier
from . import models


class InventoryItemSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), many=True)

    class Meta:
        model = models.InventoryItem
        fields = '__all__'
