from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    """
    doc for users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
