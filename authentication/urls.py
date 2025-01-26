from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.usr_login,name='login'),
    path('logout/',views.usr_logout,name='logout'),
    path('signup_successful/',views.signup_successful,name='signup_successful'),
    path('session_expired/',views.session_expired,name='session_expired')
]