from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .models import InventoryItem
from .serializers import InventoryItemSerializer
from suppliers.serializers import SupplierSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

    @action(detail=True, methods=['get'])
    def suppliers(self, request, pk=None):
        item = self.get_object()
        suppliers = item.suppliers.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_suppliers = paginator.paginate_queryset(suppliers, request)

        serializer = SupplierSerializer(paginated_suppliers, many=True)

        return paginator.get_paginated_response(serializer.data)
