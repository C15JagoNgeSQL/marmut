from django.urls import path
from MusicIndustry.views import *


app_name = 'MusicIndustry'


urlpatterns = [
    path('royalti/', show_royalti, name='royalti'),
    path('kelola-album/', kelola_album, name='kelola_album'),
    path('create-album/', create_album, name='create_album'),
    path('daftar-lagu/<str:album_id>/', daftar_lagu, name='daftar_lagu'),
    path('create-lagu/', create_lagu, name='create_lagu'),
    path('delete-lagu/<str:lagu_id>/', delete_lagu, name='delete_lagu'),
    path('delete-album/<str:album_id>/', delete_album, name='delete_album')
]