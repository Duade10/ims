from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet

router = DefaultRouter()
router.register(r'', InventoryItemViewSet, basename='inventory_items')

urlpatterns = [
    path('', include(router.urls)),
]
