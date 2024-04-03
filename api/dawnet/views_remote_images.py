from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from byo_network_hub.models import RemoteImage
from .serializers import RemoteImageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class RemoteImageListView(generics.ListCreateAPIView):
    queryset = RemoteImage.objects.all()
    serializer_class = RemoteImageSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            # For GET requests, allow any permissions (i.e., no authentication required)
            permission_classes = [permissions.AllowAny]
        # Return the permission instances
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        if self.request.method == "POST":
            authentication_classes = [JWTAuthentication]
        else:
            # For GET requests, no authentication is applied
            authentication_classes = []
        # Return the authentication instances
        return [auth() for auth in authentication_classes]

    def perform_create(self, serializer):
        # Automatically set the remote_author to the user's email
        serializer.save(remote_author=self.request.user.email)


class RemoteImageDeleteView(generics.DestroyAPIView):
    queryset = RemoteImage.objects.all()
    serializer_class = RemoteImageSerializer
    lookup_field = "id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        # Assuming request.user.email holds the email of the authenticated user
        user_email = self.request.user.email

        if instance.remote_author != user_email:
            # If the emails don't match, raise PermissionDenied
            raise PermissionDenied({"detail": "You do not have permission to delete this image."})

        # If the check passes, proceed with the default deletion process
        super().perform_destroy(instance)
