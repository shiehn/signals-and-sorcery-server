'''Collection of filters for user app'''
import django_filters
from django.utils.translation import gettext as _

from common.helper import BOOLEAN_CHOICES
from common.mixins import FilterPlaceholderSetup

from .models import CustomUser, CustomUserRole


# pylint: disable=too-few-public-methods
class CustomUserFilter(FilterPlaceholderSetup, django_filters.FilterSet):
    '''Filter for user'''
    email = django_filters.CharFilter(
        label=_('Email'), field_name='email', lookup_expr='icontains')
    role = django_filters.ChoiceFilter(
        label=_('Role'), choices=CustomUserRole.choices)
    is_active = django_filters.ChoiceFilter(
        label=_('Active'), choices=BOOLEAN_CHOICES)

    def __init__(self, *args, **kwargs):
        '''Init the filter with placeholders'''
        super().__init__(*args, **kwargs)

        for f_field in self.form.fields:
            field = self.form.fields[f_field]
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['data-placeholder'] = field.label


    class Meta:  # pylint: disable=too-few-public-methods
        '''Meta for filter'''
        model = CustomUser
        fields = ('email', 'role', 'is_active')
