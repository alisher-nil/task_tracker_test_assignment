from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from api.views import TasksViewSet, UserSignUpView

app_name = "api"

auth_urlpatterns = [
    path("register/", UserSignUpView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
]

task_router = DefaultRouter()
task_router.register(r"", TasksViewSet, basename="tasks")

urlpatterns = [
    path("auth/", include(auth_urlpatterns)),
    path("tasks/", include(task_router.urls)),
]
