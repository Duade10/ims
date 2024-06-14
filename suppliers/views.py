from rest_framework.viewsets import ViewSet

from . import models, serializers


class SupplierViewSet(ViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
