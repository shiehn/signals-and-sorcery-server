from rest_framework import generics
from byo_network_hub.models import RemoteSource
from .serializers import RemoteSourceSerializer


class RemoteSourceListView(generics.ListCreateAPIView):
    queryset = RemoteSource.objects.all()
    serializer_class = RemoteSourceSerializer
