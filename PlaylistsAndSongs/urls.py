from django.urls import path
from main import views
from main.views import show_main, login_user, logout_user, show_dashboard
from main.views import *
from main.views import temporary_chart_detail_view, temporary_lihat_chart_view, temporary_crud_user_playlist_view, temporary_r_podcast_view
from PlaylistsAndSongs.views import show_kelola_playlist, show_tambah_playlist, show_ubah_playlist, show_detail_playlist, show_tambah_lagu

app_name = 'PlaylistAndSongs'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('kelola-playlist/', show_kelola_playlist, name='kelola_playlist'),
    path('tambah-playlist/', show_tambah_playlist, name='tambah_playlist'),
    path('ubah-playlist/', show_ubah_playlist, name='ubah_playlist'),
    path('detail-playlist/', show_detail_playlist, name='detail_playlist'),
    path('tambah-lagu/', show_tambah_lagu, name='tambah_lagu'),
]