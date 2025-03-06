from ..models import StreamPlatform, WatchList
from .serializers import StreamPlatformSerializer, WatchListSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


class WatchListView(APIView):
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
