from django.urls import path
from main import views
from main.views import show_main, login_user, logout_user, show_dashboard
from main.views import *
from main.views import temporary_chart_detail_view, temporary_lihat_chart_view, temporary_r_podcast_view, temporary_crud_kelola_podcast_view


app_name = 'main'

urlpatterns = [
    # path('', show_main, name='show_main'),
    path('login/', login_user, name='login'), #sesuaikan dengan nama fungsi yang dibuat'
    path('logout/', logout_user, name='logout'),
    path('', show_dashboard, name='dashboard'),
    path('chart_detail/', temporary_chart_detail_view, name='chart_detail'),
    path('lihat_chart/', temporary_lihat_chart_view, name='lihat_chart'),
    path('crud_kelola_podcast/', temporary_crud_kelola_podcast_view, name='crud_kelola_podcast'),
    path('r_podcast/', temporary_r_podcast_view, name='r_podcast'),
]