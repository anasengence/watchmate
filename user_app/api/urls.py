from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import RegisterView

urlpatterns = [
    path("login/", obtain_auth_token, name="Login"),
    path("register/", RegisterView.as_view(), name="Register"),
]
