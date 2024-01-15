'''Collection of views for user app'''
from django.conf import settings

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

from common.mixins import (
    FilterListViewMixin, OrderListViewMixin, SuperuserAccessOnly
)

from .filters import CustomUserFilter
from .forms import CustomUserForm
from .models import CustomUser


# pylint: disable=too-many-ancestors
class UserListView(FilterListViewMixin, OrderListViewMixin, SuperuserAccessOnly,ListView):
    '''User list view'''
    queryset = CustomUser.objects.all()
    template_name = 'user/list.html'
    paginate_by = settings.OBJECTS_PER_PAGE
    ordering = ['email']
    ordering_fields = [
        'username', 'email', 'date_joined', 'is_active', 'is_superuser'
    ]
    filterset_class = CustomUserFilter


class UserCreateView(SuperuserAccessOnly, CreateView):
    '''User create view'''
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'user/change.html'
    success_url = reverse_lazy('user:user-list')

    def form_valid(self, form: CustomUserForm) -> HttpResponseRedirect:
        '''Form valid method'''
        password = form.cleaned_data.get('password')
        user = form.instance
        user.set_password(password)
        user.save()

        return super().form_valid(form)


class UserUpdateView(SuperuserAccessOnly, UpdateView):
    '''User update view'''
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'user/change.html'
    success_url = reverse_lazy('user:user-list')
