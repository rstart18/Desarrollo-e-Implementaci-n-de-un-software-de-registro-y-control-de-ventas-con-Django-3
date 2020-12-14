from django.urls import path,include
from gestionVenta import views

urlpatterns = [
    path('', views.sell),
    path('box/',views.box),
    path('sales/<int:pag>',views.sales),
    path('view_sale/<int:id_sale>',views.view_sales),
    path('fact',views.fact_in_warehaouse),
    path('search_products/',views.search_products),
    path('search_products/', include('Cart.urls')),
    path('search_clients/',views.search_clients),
]