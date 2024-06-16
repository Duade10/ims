from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from inventoryitems.models import InventoryItem
from inventoryitems.serializers import InventoryItemSerializer
from .models import Supplier
from .serializers import SupplierSerializer

User = get_user_model()


class SupplierAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='testuser@example.com', password='testpassword', first_name='Test', last_name='User'
        )
        self.token = RefreshToken.for_user(self.user).access_token

        self.supplier = Supplier.objects.create(name="Test Supplier", contact_information="123 Test St")

        self.item1 = InventoryItem.objects.create(
            name="Item 1", description="Description 1", price=100.00
        )
        self.item2 = InventoryItem.objects.create(
            name="Item 2", description="Description 2", price=200.00
        )

        self.supplier.items.add(self.item1, self.item2)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_list_suppliers(self):
        url = reverse('supplier-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve_supplier(self):
        url = reverse('supplier-detail', args=[self.supplier.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = SupplierSerializer(self.supplier)
        self.assertEqual(response.data, serializer.data)

    def test_filter_and_search_suppliers(self):
        url = reverse('supplier-list')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    def test_list_items_for_supplier(self):
        url = reverse('supplier-items', args=[self.supplier.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.supplier.items.all()
        factory = APIRequestFactory()
        request = factory.get(url)
        request = Request(request)

        paginator = PageNumberPagination()
        paginated_items = paginator.paginate_queryset(items, request)
        serializer = InventoryItemSerializer(paginated_items, many=True)

        self.assertEqual(response.data, paginator.get_paginated_response(serializer.data).data)
