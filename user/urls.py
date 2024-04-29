from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationApiView,logout_view


urlpatterns = [
    path('login/',obtain_auth_token,name='login'),
    path('register/',UserRegistrationApiView.as_view(),name='register'),
    path('logout/',logout_view,name='logout'),
]
