from rest_framework import generics, permissions
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


class RemoteImageDeleteView(generics.DestroyAPIView):
    queryset = RemoteImage.objects.all()
    serializer_class = RemoteImageSerializer
    lookup_field = "id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
