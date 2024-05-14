from django.urls import path
from ChartAndPodcast.views import *



app_name = 'ChartAndPodcast'


urlpatterns = [
    path('chart_detail/', chart_detail_view, name='chart_detail'),
    path('lihat_chart/', lihat_chart_view, name='lihat_chart'),
    path('crud_kelola_podcast/', crud_kelola_podcast_view, name='crud_kelola_podcast'),
    path('r_podcast/', r_podcast_view, name='r_podcast'),
]