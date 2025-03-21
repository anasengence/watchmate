from ..models import StreamPlatform, WatchList, Review
from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from .serializers import ReviewSerializer, StreamPlatformSerializer, WatchListSerializer
from .throttles import ReviewListThrottle, ReviewCreateThrottle
from .pagination import WatchListPagination
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import (
    UserRateThrottle,
    AnonRateThrottle,
    ScopedRateThrottle,
)
from rest_framework.authentication import BasicAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class UsernameReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        username = self.request.query_params.get("username")
        return Review.objects.filter(review_user__username=username)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        review_user = self.request.user
        watchlist = WatchList.objects.get(pk=pk)
        review_queryset = Review.objects.filter(
            watchlist=watchlist, review_user=review_user
        )

        if review_queryset.exists():
            raise ValidationError({"error": "You have already reviewed this movie!"})

        if watchlist.no_of_reviews == 0:
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating * watchlist.no_of_reviews
                + serializer.validated_data["rating"]
            ) / (watchlist.no_of_reviews + 1)

        watchlist.no_of_reviews += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(watchlist=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrReadOnly]
    # authentication_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


class WatchListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListPagination
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["avg_rating"]
    filterset_fields = ["titile", "platform__name"]
    search_fields = ["titile", "platform__name"]


# class WatchListView(APIView):
#     permission_classes = [AdminOrReadOnly]


#     def get(self, request):
#         lists = WatchList.objects.all()
#         serializer = WatchListSerializer(lists, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            obj = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "The WatchList does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = WatchListSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            obj = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response(
                {"error": "The WatchList does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = WatchListSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = WatchList.objects.get(pk=pk)
        obj.delete()
        return Response(
            {"message": "WatchList deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


class StreamPlatformListView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    # throttle_classes = [ScopedRateThrottle]
    throttle_scope = "stream"

    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "The StreamPlatform does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response(
                {"error": "The StreamPlatform does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(
            {"message": "StreamPlatform deleted successfully!"},
            status=status.HTTP_204_NO_CONTENT,
        )


# @api_view(['GET', 'POST'])
# def WatchList_list(request):
#     if request.method == 'GET':
#         WatchLists = WatchList.objects.all()
#         serializer = WatchListSerializer(WatchLists, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def WatchList_detail(request, pk):
#     if request.method == 'GET':
#         try:
#             WatchList = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error': 'The WatchList does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(WatchList)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         try:
#             WatchList = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error': 'The WatchList does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchListSerializer(WatchList, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         WatchList = WatchList.objects.get(pk=pk)
#         WatchList.delete()
#         return Response({'message': 'WatchList deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
