from django.urls import include, path

# from rest_framework.routers import DefaultRouter
from .views import UserSignUpView

app_name = "api"

# auth_router = DefaultRouter()
# auth_router.register("", AuthView, basename="register")

auth_urlpatterns = [path("register/", UserSignUpView.as_view(), name="register")]

urlpatterns = [path("auth/", include(auth_urlpatterns))]
