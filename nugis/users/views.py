from django.contrib.auth.models import User
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView

from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserList(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetail(RetrieveUpdateAPIView):
    """
    doc for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
