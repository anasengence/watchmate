from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password3 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email" ,"password", "password3")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], email=validated_data["email"] ,password=validated_data["password"]
        )
        return user

    def validate(self, data):
        if data["password"] != data["password3"]:
            raise serializers.ValidationError({"password": "Passwords must match"})
        elif User.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        return data
