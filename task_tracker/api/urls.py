from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import UserSignUpView

app_name = "api"

auth_urlpatterns = [
    path("register/", UserSignUpView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
]

urlpatterns = [path("auth/", include(auth_urlpatterns))]
