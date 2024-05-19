from django.urls import path
from ChartAndPodcast.views import *



app_name = 'ChartAndPodcast'


urlpatterns = [
    path('chart_detail/<str:id_playlist>', chart_detail_view, name='chart_detail'),
    path('lihat_chart/', lihat_chart_view, name='lihat_chart'),
    path('crud_kelola_podcast/', crud_kelola_podcast_view, name='crud_kelola_podcast'),
    path('crud_kelola_podcast/<str:podcast_data>/', crud_episode_view, name='crud_episode'),
    path('r_podcast/', r_podcast_view, name='r_podcast'),
    path('list_podcast/', list_podcast_view, name='list_podcast'),    
    path('r_podcast/<str:podcast_id>/', r_podcast_view, name='r_podcast'),
    path('delete_episode', delete_episode_view, name='delete_episode'),
    path('create_episode/<uuid:uuid>', create_episode, name='create_episode'),
    path('delete_podcast', delete_podcast_view, name='delete_podcast'),
    path('create_podcast', create_podcast, name='create_podcast'),
]