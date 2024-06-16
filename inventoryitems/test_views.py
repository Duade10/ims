from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from suppliers.models import Supplier
from suppliers.serializers import SupplierSerializer
from .models import InventoryItem
from .serializers import InventoryItemSerializer

User = get_user_model()


class InventoryItemAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email='testuser@example.com', password='testpassword', first_name='Test', last_name='User'
        )
        self.token = RefreshToken.for_user(self.user).access_token

        self.supplier1 = Supplier.objects.create(name="Supplier 1", contact_information="123 Supplier St")
        self.supplier2 = Supplier.objects.create(name="Supplier 2", contact_information="456 Supplier St")

        self.item1 = InventoryItem.objects.create(
            name="Item 1", description="Description 1", price=100.00
        )
        self.item2 = InventoryItem.objects.create(
            name="Item 2", description="Description 2", price=200.00
        )

        self.item1.suppliers.add(self.supplier1, self.supplier2)
        self.item2.suppliers.add(self.supplier1)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_list_inventory_items(self):
        url = reverse('inventoryitem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = InventoryItem.objects.all()
        serializer = InventoryItemSerializer(items, many=True)
        self.assertEqual(response.data['results'], serializer.data)

    def test_retrieve_inventory_item(self):
        url = reverse('inventoryitem-detail', args=[self.item1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = InventoryItemSerializer(self.item1)
        self.assertEqual(response.data, serializer.data)

    def test_search_inventory_items(self):
        url = reverse('inventoryitem-list')
        response = self.client.get(url, {'search': 'Item 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0)

    def test_filter_inventory_items_by_price(self):
        url = reverse('inventoryitem-list')
        response = self.client.get(url, {'price__gte': 150})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(float(item['price']) >= 150.00 for item in response.data['results']))

    def test_list_suppliers_for_inventory_item(self):
        url = reverse('inventoryitem-suppliers', args=[self.item1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        suppliers = self.item1.suppliers.all()
        factory = APIRequestFactory()
        request = factory.get(url)
        request = Request(request)

        paginator = PageNumberPagination()
        paginated_suppliers = paginator.paginate_queryset(suppliers, request)
        serializer = SupplierSerializer(paginated_suppliers, many=True)

        self.assertEqual(response.data, paginator.get_paginated_response(serializer.data).data)


if __name__ == "__main__":
    import unittest

    unittest.main()
