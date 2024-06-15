from rest_framework import serializers
from . import models
from suppliers.models import Supplier


class InventoryItemSerializer(serializers.ModelSerializer):
    suppliers = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), many=True)

    class Meta:
        model = models.InventoryItem
        fields = '__all__'
