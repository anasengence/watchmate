from django.urls import path
from .views import WatchListDetailView, WatchListView, StreamPlatformListView, StreamPlatformDetailView

urlpatterns = [
    path("list/", WatchListView.as_view(), name="WatchList-list"),
    path("list/<int:pk>/", WatchListDetailView.as_view(), name="WatchList-detail"),
    path("stream/", StreamPlatformListView.as_view(), name="Stream-list"),
    path("stream/<int:pk>/", StreamPlatformDetailView.as_view(), name="Stream-detail"),
]
