"""
URL configuration for vendor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from . import views

urlpatterns = [
    # Vendor Profile Management
    path('admin/', admin.site.urls),
    path('api/vendors/', views.create_vendor, name='create_vendor'),
    path('api/vendors/', views.list_vendors, name='list_vendors'),
    path('api/vendors/<int:vendor_id>/', views.vendor_details, name='vendor_details'),

    # Purchase Order Tracking
    path('api/purchase_orders/', views.create_purchase_order, name='create_purchase_order'),
    path('api/purchase_orders/', views.list_purchase_orders, name='list_purchase_orders'),
    path('api/purchase_orders/<int:po_id>/', views.purchase_order_details, name='purchase_order_details'),

    # Vendor Performance Evaluation
    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),

    # Update Acknowledgment Endpoint
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
]

