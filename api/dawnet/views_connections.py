from rest_framework import generics
from django.shortcuts import get_object_or_404
from byo_network_hub.models import Connection
from .serializers import ConnectionSerializer


class ConnectionListCreateView(generics.ListCreateAPIView):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class ConnectionListByMasterTokenView(generics.ListAPIView):
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        master_token = self.kwargs["master_token"]
        return Connection.objects.filter(master_token=master_token)


class ConnectionDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ConnectionSerializer

    def get_object(self):
        master_token = self.kwargs["master_token"]
        connection_token = self.kwargs["connection_token"]
        return get_object_or_404(
            Connection, master_token=master_token, connection_token=connection_token
        )
