from rest_framework import generics
import json

from byo_network_hub.models import ComputeContract
from dawnet_client import SentryEventLogger, DNSystemType, DNTag, DNMsgStage
from api.serializers import ComputeContractSerializer

dn_tracer = SentryEventLogger(service_name=DNSystemType.DN_API_SERVER.value)

class ComputeContractListCreateView(generics.ListCreateAPIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    queryset = ComputeContract.objects.all()
    serializer_class = ComputeContractSerializer

    def perform_create(self, serializer):
        # This will use the 'id' from the validated_data if it exists
        try:
            serializer.save()

            if serializer.validated_data.get('id'):
                dn_tracer.log_event(str(serializer.validated_data.get('id')), {
                    DNTag.DNMsgStage.value: DNMsgStage.SAVE_CONTRACT.value,
                    DNTag.DNMsg.value: "success",
                })
        except Exception as e:
            if serializer.validated_data.get('id'):
                dn_tracer.log_error(str(serializer.validated_data.get('id')), {
                    DNTag.DNMsgStage.value: DNMsgStage.SAVE_CONTRACT.value,
                    DNTag.DNMsg.value: str(e),
                })

        if serializer.validated_data.get('id'):
            dn_tracer.log_event(str(serializer.validated_data.get('id')), {
                DNTag.DNMsgStage.value: DNMsgStage.SAVE_CONTRACT.value,
                DNTag.DNMsg.value: "success",
            })

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ComputeContractRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    queryset = ComputeContract.objects.all()
    serializer_class = ComputeContractSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        print("Incoming PUT data:", json.dumps(request.data))
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print("Incoming PATCH data:", json.dumps(request.data))
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print("Incoming DELETE request")
        return super().delete(request, *args, **kwargs)
