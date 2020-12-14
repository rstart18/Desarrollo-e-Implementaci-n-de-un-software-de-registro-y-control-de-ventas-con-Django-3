from django.urls import path
from Almacen import views
from gestionVenta.views import envios,processEnvio

urlpatterns = [
    path('products/catering/',views.catering),
    path('products/<int:pag>',views.products),
    path('products/inventory/<int:pag>',views.inventory),
    path('products/products_is_exist/',views.products_is_exist),
    path('products/edit/<int:product_id>',views.edit_product),
    path('products/delete/<int:product_id>', views.delete_product),
    path('products/supply/<int:product_id>', views.supply),
    path('products/search_supply/', views.search_supply),
    path('categorys/<int:pag>',views.categorys),
    path('categorys/categorys_is_exist/',views.categorys_is_exist),
    path('categorys/register',views.register_category),
    path('categorys/edit/<int:category_id>',views.edit_category),
    path('categorys/delete/<int:category_id>', views.delete_category),
    path('providers/<int:pag>',views.providers),
    path('providers/providers_is_exist/',views.providers_is_exist),
    path('providers/register',views.register_provider),
    path('providers/edit/<int:provider_id>',views.edit_provider),
    path('providers/delete/<int:provider_id>', views.delete_provider),
    path('clients/<int:pag>',views.clients),
    path('clients/clients_is_exist/',views.clients_is_exist),
    path('clients/register',views.register_client),
    path('clients/edit/<int:client_id>',views.edit_client),
    path('clients/delete/<int:client_id>', views.delete_clients),
    path('envios/<int:pag>',envios),
    path('processEnvios/<int:id_envio>',processEnvio),
]