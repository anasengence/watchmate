from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user_app.api.views import LogoutView, RegisterView

urlpatterns = [
    path("login/", obtain_auth_token, name="Login"),
    path("register/", RegisterView.as_view(), name="Register"),
    path("logout/", LogoutView.as_view(), name="Logout"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
