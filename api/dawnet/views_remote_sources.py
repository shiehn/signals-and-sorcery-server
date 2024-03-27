from rest_framework import generics
from byo_network_hub.models import RemoteSource
from .serializers import RemoteSourceSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class RemoteSourceListView(generics.ListCreateAPIView):
    queryset = RemoteSource.objects.all()
    serializer_class = RemoteSourceSerializer

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


class RemoteSourceDeleteView(generics.DestroyAPIView):
    queryset = RemoteSource.objects.all()
    serializer_class = RemoteSourceSerializer
    lookup_field = "id"
    # Apply JWT Authentication and IsAuthenticated permission to the DELETE method
    authentication_classes = [
        JWTAuthentication,
    ]
    permission_classes = [
        IsAuthenticated,
    ]
