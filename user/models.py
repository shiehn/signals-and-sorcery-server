'''Collection of models for user app'''
from django.db import models
from django.contrib.auth.models import AbstractUser

from common.helper import make_uuid

from .types import UserJSONType
from .managers import CustomUserRole, UserManager


class CustomUser(AbstractUser):
    '''CustomUser model for app with email as login field'''
    id = models.UUIDField(primary_key=True, default=make_uuid, editable=False, unique=True)
    username = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField('Email address', unique=True)
    role = models.CharField(
        choices=CustomUserRole.choices,
        max_length=20,
        default=CustomUserRole.USER
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self) -> str:
        '''Return username'''
        return '' if self.username is None else self.username

    def full_name(self) -> str:
        '''Return username'''
        return f'{self.first_name} {self.last_name}'

    def to_json(self) -> UserJSONType:
        '''Return a formatted JSON for this model'''
        return {
            'id': str(self.id),
            'email': self.email,
            'username': self.username,
            'role': self.get_role_display(),
            'first_name': self.first_name,
            'last_name': self.last_name
        }
