from django.urls import path
from PlaylistsAndSongs.views import *

app_name = 'PlaylistAndSongs'

urlpatterns = [
    path('kelola-playlist/', show_kelola_playlist, name='kelola_playlist'),
    path('tambah-playlist/', show_tambah_playlist, name='tambah_playlist'),
    path('ubah-playlist/<str:playlist_id>', show_ubah_playlist, name='ubah_playlist'),
    path('hapus-playlist/<str:playlist_id>', show_hapus_playlist, name='hapus_playlist'),
    path('detail-playlist/<str:playlist_id>', show_detail_playlist, name='detail_playlist'),
    path('tambah-lagu/<str:playlist_id>', show_tambah_lagu, name='tambah_lagu'),
    path('hapus-lagu/<str:playlist_id>/<str:id_song>', show_hapus_lagu, name='hapus_lagu'),
    path('detail-lagu/<str:song_id>', show_detail_lagu, name='detail_lagu'),
    path('play-user-playlist/', show_play_user_playlist, name='play_user_playlist'),
    path('tambah-lagu-ke-playlist/<str:id_song>', show_tambah_lagu_ke_playlist, name='tambah_lagu_ke_playlist'),
]