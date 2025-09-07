from django.urls import path, include
from .views import RegistrationView, LoginView, EmailCheckView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-check/', EmailCheckView.as_view(), name='email-check')
]