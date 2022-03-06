from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='homepage'),
    path('login', login, name='loginpage'),
    path('register', register, name='registerpage'),
    path('token-send', token_send, name='tokensend'),
    path('success', success, name='success'),
    path('verify/<auth_token>', verify, name="verify"),
    path('error', error_page, name="verify"),
    path('logout', logout, name='logoutpage'),
    path('home', login_success, name='login-success'),

]
