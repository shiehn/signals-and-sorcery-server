from rest_framework import generics
from byo_network_hub.models import RemoteImage
from .serializers import RemoteImageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class RemoteImageListView(generics.ListCreateAPIView):
    queryset = RemoteImage.objects.all()
    serializer_class = RemoteImageSerializer

    # Only apply JWT Authentication and IsAuthenticated permission to the POST method
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [
                IsAuthenticated,
            ]
            self.authentication_classes = [
                JWTAuthentication,
            ]
        return super().get_permissions()


class RemoteImageDeleteView(generics.DestroyAPIView):
    queryset = RemoteImage.objects.all()
    serializer_class = RemoteImageSerializer
    lookup_field = "id"
    # Apply JWT Authentication and IsAuthenticated permission to the DELETE method
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]
