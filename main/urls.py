from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('profile/', show_dashboard, name='dashboard'),
    path('register/', show_register, name="register"),
    path('register/user', show_register_user, name="registerUser"),
    path('register/label', show_register_label, name="registerLabel")
]