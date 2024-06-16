from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from suppliers.serializers import SupplierSerializer
from .filters import InventoryItemFilter
from .models import InventoryItem
from .serializers import InventoryItemSerializer


class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = InventoryItemFilter
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def suppliers(self, request, pk=None):
        item = self.get_object()
        suppliers = item.suppliers.all()

        search = request.GET.get('search')
        if search:
            suppliers = suppliers.filter(name__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_suppliers = paginator.paginate_queryset(suppliers, request)

        serializer = SupplierSerializer(paginated_suppliers, many=True)

        return paginator.get_paginated_response(serializer.data)
