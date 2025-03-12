from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Token.objects.create(user=user)

    def post(self, request):
        response = self.create(request)
        # token = Token.objects.get(user=response.data["id"])
        # response.data["token"] = token.key
        refresh = RefreshToken.for_user(response.data["id"])
        response.data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return response


class LogoutView(generics.DestroyAPIView):
    queryset = User.objects.all()

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
