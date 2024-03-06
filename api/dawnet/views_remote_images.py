from rest_framework import generics
from byo_network_hub.models import RemoteImage
from .serializers import RemoteImageSerializer


class RemoteImageListView(generics.ListCreateAPIView):
    queryset = RemoteImage.objects.all()
    serializer_class = RemoteImageSerializer
