from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationApiView,logout_view,CustomObtainAuthToken


urlpatterns = [
    path('login/',CustomObtainAuthToken.as_view(),name='login'),
    path('register/',UserRegistrationApiView.as_view(),name='register'),
    path('logout/',logout_view,name='logout'),
]
