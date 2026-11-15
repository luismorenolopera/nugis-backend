from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class UserList(CreateAPIView):
    """Sign up."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserDetail(RetrieveUpdateAPIView):
    """Read or update a user. Each user can only see and edit themselves."""
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class Me(RetrieveUpdateAPIView):
    """Read or update the logged-in user."""
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
