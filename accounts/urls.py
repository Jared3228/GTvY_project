# accounts/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts' #Importante

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(next_page='core:dashboard'),
        name='logout'
    ),
]
