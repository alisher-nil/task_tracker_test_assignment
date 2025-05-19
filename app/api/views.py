from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from tasks.models import Task

from .serializers import SignUpSerializer, TasksSerializer


class UserSignUpView(views.APIView):
    """
    View to handle user registration.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TasksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["completed"]
    search_fields = ["title"]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
