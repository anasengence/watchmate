from rest_framework import serializers
from ..models import StreamPlatform, WatchList, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        # exclude = ["watchlist"]
        exclude = ("watchlist",)


class WatchListSerializer(serializers.ModelSerializer):
    # Show platform name in GET requests
    platform_name = serializers.CharField(source="platform.name", read_only=True)

    # Accept platform ID in POST/PUT requests
    platform = serializers.PrimaryKeyRelatedField(
        queryset=StreamPlatform.objects.all(), write_only=True
    )

    class Meta:
        model = WatchList
        fields = "__all__"

        # exclude = ["active"]


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"


# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError('Name is too short!')
#     return value

# class WatchListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance

#     def validate(self, attrs):
#         if attrs['name'] == attrs['description']:
#             raise serializers.ValidationError('Name and Description should be different!')
#         return attrs

#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError('Name is too short!')
#         return value
