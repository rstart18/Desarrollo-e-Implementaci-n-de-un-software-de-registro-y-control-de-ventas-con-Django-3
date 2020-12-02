from django.urls import path
from Cart import views

urlpatterns = [
    path('add_cart/',views.add_product),
    path('remove_cart/',views.remove_product),
    path('clear_cart/',views.clear_cart),

]