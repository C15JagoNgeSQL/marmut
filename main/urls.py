from django.urls import path
from main import views
from main.views import show_main, login_user, logout_user, show_dashboard
from main.views import *


app_name = 'main'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('login/', login_user, name='login'), #sesuaikan dengan nama fungsi yang dibuat'
    path('logout/', logout_user, name='logout'),
    path('', show_dashboard, name='dashboard'),
    path('register/', show_register, name="register"),
    path('register/user', show_register_user, name="registerUser"),
    path('register/label', show_register_label, name="registerLabel"),
    path('tes/', tes_query, name='tes_query')
]