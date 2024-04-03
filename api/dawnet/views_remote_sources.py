from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from byo_network_hub.models import RemoteSource
from .serializers import RemoteSourceSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class RemoteSourceListView(generics.ListCreateAPIView):
    queryset = RemoteSource.objects.all()
    serializer_class = RemoteSourceSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.request.method == "POST":
            authentication_classes = [JWTAuthentication]
        else:
            authentication_classes = []
        return [auth() for auth in authentication_classes]

    def perform_create(self, serializer):
        # Automatically set the remote_author to the user's email
        serializer.save(remote_author=self.request.user.email)


class RemoteSourceDeleteView(generics.DestroyAPIView):
    queryset = RemoteSource.objects.all()
    serializer_class = RemoteSourceSerializer
    lookup_field = "id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # Assuming request.user.email holds the email of the authenticated user
        user_email = self.request.user.email

        if instance.remote_author != user_email:
            # If the emails don't match, raise PermissionDenied
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this source."}
            )

        # If the check passes, proceed with the default deletion process
        super().perform_destroy(instance)
