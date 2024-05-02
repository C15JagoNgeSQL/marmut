from django.urls import path
from MusicIndustry.views import *


app_name = 'MusicIndustry'


urlpatterns = [
    path('royalti/', show_royalti, name='royalti'),
]