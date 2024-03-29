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

    # template_name = "login.html"
    # form_class = AuthenticationForm
    # success_url = reverse_lazy("dashboard")
    # logger = logging.getLogger("django.message")
    #
    # @method_decorator(sensitive_post_parameters("password"))
    # @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    # def dispatch(self, request: WSGIRequest, *args, **kwargs) -> TemplateResponse:
    #     """Dispatch request based on authentication"""
    #     if request.user.is_authenticated:
    #         return redirect(self.success_url)
    #     # Sets a test cookie to make sure the user has cookies enabled
    #     request.session.set_test_cookie()
    #     return super().dispatch(request, *args, **kwargs)
    #
    # def form_valid(self, form: AuthenticationForm) -> HttpResponseRedirect:
    #     """Check information from the login page"""
    #     username = self.request.POST.get("username", False)
    #     password = self.request.POST.get("password", False)
    #     user = authenticate(username=username, password=password)
    #     if user.role != CustomUserRole.SUPERUSER:
    #         form.add_error("username", _("Unauthorized"))
    #         return super().form_invalid(form)
    #
    #     login(self.request, form.get_user())
    #
    #     # If the test cookie worked, go ahead and
    #     # delete it since its no longer needed
    #     if self.request.session.test_cookie_worked():
    #         self.request.session.delete_test_cookie()
    #
    #     return super().form_valid(form)

    # def get_success_url(self):
    #     # Default to "/auth/profile/" if no next parameter is provided
    #     next_url = super().get_success_url()
    #     print("STEVE: LOGIN SUCCESS: " + str(next_url))
    #     return next_url if next_url != "/" else "/auth/profile/"


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
