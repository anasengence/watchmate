from django.urls import path
from .views import (
    ReviewCreateView,
    ReviewDetailView,
    ReviewListView,
    WatchListDetailView,
    WatchListView,
    StreamPlatformListView,
    StreamPlatformDetailView,
    UsernameReviewListView,
)

urlpatterns = [
    path("list/", WatchListView.as_view(), name="WatchList-list"),
    path("list/<int:pk>/", WatchListDetailView.as_view(), name="WatchList-detail"),
    path("list/<int:pk>/reviews/", ReviewListView.as_view(), name="Review-list"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="Review-detail"),
    path(
        "list/<int:pk>/review-create/", ReviewCreateView.as_view(), name="Review-create"
    ),
    path("stream/", StreamPlatformListView.as_view(), name="Stream-list"),
    path("stream/<int:pk>/", StreamPlatformDetailView.as_view(), name="Stream-detail"),
    path(
        "reviews/",
        UsernameReviewListView.as_view(),
        name="User-Review-list",
    ),
]
