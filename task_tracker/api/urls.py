from django.urls import include, path

from .views import RegistrationView

app_name = "api"

auth_urlpatterns = [path("register/", RegistrationView.as_view(), name="register")]

urlpatterns = [path("auth/", include(auth_urlpatterns))]
