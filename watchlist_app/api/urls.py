from django.urls import path
from .views import MovieDetailView, MovieListView

urlpatterns = [
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('list/<int:pk>/', MovieDetailView.as_view(), name='movie-detail')
]
