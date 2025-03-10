from ..models import StreamPlatform, WatchList, Review
from .permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from .serializers import ReviewSerializer, StreamPlatformSerializer, WatchListSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer

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
            raise ValidationError("You have already reviewed this movie!")

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(watchlist=pk)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    # authentication_classes = [IsA]
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


class WatchListView(APIView):
    permission_classes = [AdminOrReadOnly]


    def get(self, request):
        lists = WatchList.objects.all()
        serializer = WatchListSerializer(lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailView(APIView):
    permission_classes = [AdminOrReadOnly]
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
