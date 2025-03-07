from django.urls import path
from .views import ReviewCreateView, ReviewDetailView, ReviewListView, WatchListDetailView, WatchListView, StreamPlatformListView, StreamPlatformDetailView

urlpatterns = [
    path("list/", WatchListView.as_view(), name="WatchList-list"),
    path("list/<int:pk>/", WatchListDetailView.as_view(), name="WatchList-detail"),
    path("list/<int:pk>/review/", ReviewListView.as_view(), name="Review-list"),
    path("list/review/<int:pk>/", ReviewDetailView.as_view(), name="Review-detail"),
    path("list/<int:pk>/review-create/", ReviewCreateView.as_view(), name="Review-create"),
    path("stream/", StreamPlatformListView.as_view(), name="Stream-list"),
    path("stream/<int:pk>/", StreamPlatformDetailView.as_view(), name="Stream-detail"),
]
