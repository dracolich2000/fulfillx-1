from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('users/',views.users,name='users'),
    path('user_details/<int:user_id>',views.user_details,name='user_details'),
    path('assign_role/', views.assign_role, name='assign_role'),
    path('admin_products/',views.products,name='admin_products'),
    path('admin_sourcing_requests/',views.sourcing_requests,name='admin_sourcing_requests'),
]