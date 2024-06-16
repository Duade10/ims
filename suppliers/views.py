from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from inventoryitems.filters import InventoryItemFilter
from inventoryitems.serializers import InventoryItemSerializer
from .models import Supplier
from .serializers import SupplierSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'contact_information']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        supplier = self.get_object()
        items = supplier.items.all()

        filterset = InventoryItemFilter(request.GET, queryset=items)
        if filterset.is_valid():
            items = filterset.qs

        search = request.GET.get('search')
        if search:
            items = items.filter(name__icontains=search)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_items = paginator.paginate_queryset(items, request)

        serializer = InventoryItemSerializer(paginated_items, many=True)

        return paginator.get_paginated_response(serializer.data)
