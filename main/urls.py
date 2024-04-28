from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('profile/', show_dashboard, name='dashboard'),
]