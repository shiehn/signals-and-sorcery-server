'''Collection of managers for user'''
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserRole(models.TextChoices):
    '''
    The models is set there because managers is included inside models
    So we cannot include models in there
    Enumeration for the available role of a user
    '''
    USER = 'user', _('user')
    SUPERUSER = 'superuser', _('superuser')


class UserManager(BaseUserManager):
    '''Define a model manager for User model with no username field.'''
    use_in_migrations = True

    def _create_user(self, email: str, password: str, **extra_fields) -> 'CustomUser':
        '''Create and save a User with the given email and password.'''
        if not email:
            raise ValueError(_('EmailMandatory'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> 'CustomUser':
        '''Create and save a regular User with the given email and password.'''
        extra_fields.setdefault('role', CustomUserRole.USER)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> 'CustomUser':
        '''Create and save a SuperUser with the given email and password.'''
        extra_fields.setdefault('role', CustomUserRole.SUPERUSER)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('StaffMuBeSet'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('SuperUserMustBeSet'))

        return self._create_user(email, password, **extra_fields)
