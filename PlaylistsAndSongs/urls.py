from django.urls import path
from PlaylistsAndSongs.views import *

app_name = 'PlaylistAndSongs'

urlpatterns = [
    path('kelola-playlist/', show_kelola_playlist, name='kelola_playlist'),
    path('tambah-playlist/', show_tambah_playlist, name='tambah_playlist'),
    path('ubah-playlist/', show_ubah_playlist, name='ubah_playlist'),
    path('detail-playlist/', show_detail_playlist, name='detail_playlist'),
    path('tambah-lagu/', show_tambah_lagu, name='tambah_lagu'),
    path('detail-lagu/', show_detail_lagu, name='detail_lagu'),
    path('play-user-playlist/', show_play_user_playlist, name='play_user_playlist'),
    path('tambah-lagu-ke-playlist/', show_tambah_lagu_ke_playlist, name='tambah_lagu_ke_playlist'),
]