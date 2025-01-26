from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('staff_dashboard/',views.staff_dashboard,name='staff_dashboard'),
    path('staff_products/',views.products,name='staff_products'),
    path('add_product/',views.add_product,name='add_product'),
    path('update_product/<int:product_id>/',views.update_product,name='update_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('staff_sourcing_requests/',views.sourcing_requests,name='staff_sourcing_requests'),
    path('update_sourcing_request_status/',views.update_sourcing_req_status,name='update_sourcing_req_status'),
    path('upload_products_csv',views.upload_products_csv,name='upload_products_csv')
]