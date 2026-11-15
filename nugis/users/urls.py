from django.urls import path

from .views import Me, UserDetail, UserList

urlpatterns = [
    path('me', Me.as_view(), name='user-me'),
    path('user/<int:pk>', UserDetail.as_view(), name='user-detail'),
    path('user', UserList.as_view(), name='user-list'),
]
