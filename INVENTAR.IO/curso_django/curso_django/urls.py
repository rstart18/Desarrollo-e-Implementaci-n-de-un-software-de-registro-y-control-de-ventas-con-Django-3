"""curso_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from curso_django import views
from Usuarios.views import login_request, registration_client
from django.conf import settings
from django.conf.urls.static import static
from datetime import datetime
from gestionVenta.views import confirmEnvio
from curso_django.report_inventory_pdf import ReporteProductosPDF
from curso_django.report_sales_pdf import ReporteVentasPDF

urlpatterns = [
    path('admin/', admin.site.urls),
    path('unauthorized/',views.unathorized),
    path('',views.home,name='home'),
    path('home/',views.home,name='home'),
    path('acercade/',views.acercade,name='acercade'),
    path('shop/',views.shop,name='shop'),
    path('cart/',views.cart,name='cart'),
    path('purchases/',views.purchases,name='purchases'),
    path('view_purchases/<int:id_purchase>',views.view_purchases,name='view_purchases'),
    path('confirmCreditCard/',views.confirmCreditCard),
    path('addCreditCard/',views.addCreditCard),
    path('confirmEnvio/<int:id_envio>',confirmEnvio),
    path('login/',login_request,name='login'),
    path('register/',registration_client,name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard),
    path('sell/',include('gestionVenta.urls')),
    path('warehouse/',include('Almacen.urls')),
    path('users/',include('Usuarios.urls')),
    path('report_inventory/',views.report_inventory),
    path('view_report_inventory/',views.view_report_inventory),
    path('report_sales/',views.report_sales),
    path('view_report_sales/', views.view_report_sales),
    path('reporte/inventario',ReporteProductosPDF.as_view()),
    path('reporte/ventas',ReporteVentasPDF.as_view()),
    path('cuadrado/<int:n>', views.cuadrado),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
