from django.urls import path
from main.views import show_main, login_user, logout_user
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('login/', login_user, name='login'), #sesuaikan dengan nama fungsi yang dibuat'
    path('logout/', logout_user, name='logout'),
    path('profile/', show_dashboard, name='dashboard'),
]