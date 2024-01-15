'''Collection of urls for user app'''
from django.urls import path

from .views import UserCreateView, UserListView, UserUpdateView


app_name = 'customuser'

# pylint: disable=invalid-name
urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/new/', UserCreateView.as_view(), name='user-create'),
    path('users/<uuid:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]
