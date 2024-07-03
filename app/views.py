"""Collection of views for main app"""

import logging

from django.shortcuts import redirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from user.models import CustomUserRole

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class LoginView(FormView):
    """Login view"""


class LogoutView(RedirectView):
    """Logout view"""

    url = reverse_lazy("login")

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponseRedirect:
        """Logout user"""
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view"""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs) -> RequestContext:
        """Prepare the context of the main dashboard"""
        context = super().get_context_data(**kwargs)
        return context


@login_required
def profile(request):
    # This view requires the user to be logged in
    return render(request, "user_profile.html", {"user": request.user})
