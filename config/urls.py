from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/inventory-items/', include('inventoryitems.urls')),
    path('api/users/', include('users.urls'))
]
