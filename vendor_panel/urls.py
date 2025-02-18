from django.urls import path
from . import views

urlpatterns = [
    path('vendor_dashboard/',views.vendor_dashboard,name='vendor_dashboard'),
    path('vendor_products/',views.products,name='vendor_products'),
    path('vendor_update_inventory/', views.update_inventory, name='vendor_update_inventory'),
    path('vendor_orders',views.orders,name='vendor_orders')
]