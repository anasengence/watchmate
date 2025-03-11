from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

    def post(self, request):
        response = self.create(request)
        token = Token.objects.get(user=response.data["id"])
        response.data["token"] = token.key
        return response
