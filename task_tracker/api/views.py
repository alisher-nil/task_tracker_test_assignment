from django.contrib.auth import get_user_model
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import SignUpSerializer

User = get_user_model()


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
