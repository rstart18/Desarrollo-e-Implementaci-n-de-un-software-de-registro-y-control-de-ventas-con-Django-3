from django.urls import path,include
from gestionVenta import views

urlpatterns = [
    path('', views.sell),
    path('search_products/',views.search_products),
    path('search_products/', include('Cart.urls')),
    path('search_clients/',views.search_clients),
]