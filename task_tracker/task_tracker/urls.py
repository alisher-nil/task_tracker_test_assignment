from api.urls import urlpatterns as api_urlpatterns
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urlpatterns)),
]
