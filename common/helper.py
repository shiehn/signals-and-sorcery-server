'''Collection of helpers'''
import uuid

from enum import Enum
from typing import Any, Dict, List, Tuple

from django.utils.translation import gettext_lazy as _


BOOLEAN_CHOICES = [(1, _('Yes')), (0, _('No'))]

def make_uuid() -> uuid.UUID:
    '''
    Returns a UUID V4 for postgres based models

    Example:
    class User(models.Model):
        id = models.UUIDField(primary_key=True, default=make_uuid)
    '''
    return uuid.uuid4()


def str_to_uuid(id_str: str) -> uuid.UUID:
    '''Transform a sring to a valid UUID'''
    return uuid.UUID(f'{id_str.strip()}')


class BaseEnum(Enum):
    '''
    Creates a new base class for Enum

    Example:

    class Provider(BaseEnum):
        TRADITIONAL = 'traditional'
        FACEBOOK = 'facebook'

    class User(models.Model):
        id = models.UUIDField(primary_key=True, default=make_uuid)
        provider = models.CharField(
            max_length=50,
            choices=Provider.choices(),
            default=Provider.TRADITIONAL
        )
    '''
    @classmethod
    def choices(cls) -> Tuple[Any, Any]:
        '''Returns tuples for models'''
        return tuple((x.value, x.value) for x in cls)


    @classmethod
    def array_of_choices(cls) -> List[Any]:
        '''Returns all possible choices in an array'''
        return list((x.value for x in cls))


def get_languages() -> Dict[str, str]:
    '''Get handled languages'''
    return (
        ('en', _('en')),
        ('fr', _('fr')),
    )


def get_languages_array() -> List[str]:
    '''Get handled languages in an array'''
    languages = []
    for lang in get_languages():
        languages.append(lang[0])
    return languages
