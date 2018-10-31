from .views import UserList, UserDetail
from django.urls import path


urlpatterns = [
    path(
        'user/<int:pk>',
        UserDetail.as_view(),
        name='user-detail'
    ),
    path(
        'user',
        UserList.as_view(),
        name='user-list'
    )
]
