# your_project/custom_adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return f"{settings.FRONTEND_URL}/?token={token}"
