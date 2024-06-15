from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Supplier
from .serializers import SupplierSerializer
from rest_framework import viewsets
from inventoryitems.serializers import InventoryItemSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        supplier = self.get_object()
        items = supplier.items.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_items = paginator.paginate_queryset(items, request)

        serializer = InventoryItemSerializer(paginated_items, many=True)

        return paginator.get_paginated_response(serializer.data)
