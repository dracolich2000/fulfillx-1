from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/',views.usr_dashboard,name='usr_dashboard'),
    path('custom_products/',views.custom_products,name='custom_products'),
    path('find_products/',views.find_products,name='find_products'),
    path('import_list/',views.import_list,name='import_list'),
    path('manage_store/',views.manage_store,name='manage_store'),
    path('my_products/',views.my_products,name='my_products'),
    path('view_product/<int:product_id>',views.view_product,name='user_view_product'),
    path('sourcing/',views.sourcing,name='user_sourcing'),
    path('new_sourcing_request',views.new_sourcing_request,name='new_sourcing_request'),
    path('shopify/auth/', views.shopify_auth, name='shopify_auth'),
    path('shopify/callback/', views.shopify_callback, name='shopify_callback'),
    path('pust_to_shopify/',views.push_to_shopify,name='push_to_shopify'),
    path('delete-store/<int:store_id>/', views.delete_store, name='delete_store'),
    path('user_orders/',views.orders,name='user_orders'),
    path('fetch_shopify_orders',views.fetch_and_store_shopify_orders,name='fetch_shopify_orders')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)