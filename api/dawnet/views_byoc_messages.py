import uuid

from dawnet_client import SentryEventLogger, DNSystemType, DNTag, DNMsgStage

from django.db.models import Max
from rest_framework import status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from byo_network_hub.models import BYOCMessageState, BYOCMessageStates

from api.serializers import BYOCMessageStateSerializer

dn_tracer = SentryEventLogger(service_name=DNSystemType.DN_API_SERVER.value)

class SendMessageView(views.APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, *args, **kwargs):
        # Deserialize input data
        serializer = BYOCMessageStateSerializer(data=request.data)
        if serializer.is_valid():
            # Check if a message with the same token and PENDING or PROCESSING status exists
            token = serializer.validated_data.get('token')
            existing_message = BYOCMessageState.objects.filter(
                token=token,
                status__in=[BYOCMessageStates.PENDING, BYOCMessageStates.PROCESSING]
            ).first()

            if existing_message:
                # If a message with the token is already pending or processing, return an error
                dn_tracer.log_error(str(token), {
                    DNTag.DNMsgStage.value: DNMsgStage.SET_MSG_PENDING.value,
                    DNTag.DNMsg.value: "message with the token is already pending or processing",
                })

                return Response(
                    {'error': 'A message with the given token is already being processed.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # If no existing message is found, proceed to save the new state
            message_state = serializer.save(status=BYOCMessageStates.PENDING)

            dn_tracer.log_event(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.SET_MSG_PENDING.value,
                DNTag.DNMsg.value: "success",
            })

            return Response({'id': message_state.id}, status=status.HTTP_201_CREATED)

        # If the input data was not valid, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMessageResponseView(views.APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def get(self, request, id, token, *args, **kwargs):
        try:
            message_state = BYOCMessageState.objects.get(id=id, token=token)
            return Response(BYOCMessageStateSerializer(message_state).data)
        except BYOCMessageState.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AbortMessagesView(views.APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, token, *args, **kwargs):
        try:
            # Check if the record exists
            if not BYOCMessageState.objects.filter(token=token).exists():
                dn_tracer.log_error(str(token), {
                    DNTag.DNMsgStage.value: DNMsgStage.ABORT_MSG.value,
                    DNTag.DNMsg.value: "not found",
                })

                return Response({'error': 'Record not found.'}, status=status.HTTP_404_NOT_FOUND)

            # Update the record
            affected_rows = BYOCMessageState.objects.filter(token=token).update(status='aborted')

            # Check if any rows were affected
            if affected_rows == 0:
                dn_tracer.log_error(str(token), {
                    DNTag.DNMsgStage.value: DNMsgStage.ABORT_MSG.value,
                    DNTag.DNMsg.value: "not found",
                })

                return Response({'error': 'No records updated.'}, status=status.HTTP_404_NOT_FOUND)

            dn_tracer.log_event(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.ABORT_MSG.value,
                DNTag.DNMsg.value: "success",
            })

            return Response({'aborted': affected_rows}, status=status.HTTP_200_OK)

        except Exception as e:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.ABORT_MSG.value,
                DNTag.DNMsg.value: str(e),
            })
            # Handle unexpected errors
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Consumer Views
class ReplyToMessageView(views.APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, *args, **kwargs):
        message_id = request.data.get('id')
        token = request.data.get('token')

        try:
            message_state = BYOCMessageState.objects.get(id=message_id, token=token)

            #TODO THIS WORRIES ME, WHEN SHOULD IT EVER GO FROM PENDING TO COMPLETED?
            if message_state.status != BYOCMessageStates.PENDING and message_state.status != BYOCMessageStates.PROCESSING:
                dn_tracer.log_error(str(token), {
                    DNTag.DNMsgStage.value: DNMsgStage.REPLY_TO_MSG.value,
                    DNTag.DNMsg.value: "Message is not in a state that allows updating: msg_id: " + str(message_id) + " status: " + str(message_state.status),
                })

                return Response({"detail": "Message is not in a state that allows updating."},
                                status=status.HTTP_409_CONFLICT)

            # Assuming the request will not try to update the `id` and `token`
            request.data.pop('id', None)
            request.data.pop('token', None)

            serializer = BYOCMessageStateSerializer(message_state, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                dn_tracer.log_event(str(token), {
                    DNTag.DNMsgStage.value: DNMsgStage.REPLY_TO_MSG.value,
                    DNTag.DNMsg.value: "success",
                })

                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except BYOCMessageState.DoesNotExist:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.REPLY_TO_MSG.value,
                DNTag.DNMsg.value: "not found. msg id: " + str(message_id),
            })

            return Response({"detail": "Message not found."}, status=status.HTTP_404_NOT_FOUND)


class GetLatestPendingMessagesView(views.APIView):
    authentication_classes = []  # Disables authentication
    permission_classes = []  # Disables permission

    #TODO: This is a hack, we need to figure out how to get the latest message for each token

    def get(self, request, *args, **kwargs):
        # Get the latest message for each token where status is 'pending'
        latest_messages = BYOCMessageState.objects \
            .filter(status=BYOCMessageStates.PENDING) \
            .order_by('token', '-created_at') \
            .distinct('token')

        serializer = BYOCMessageStateSerializer(latest_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateMessageStatusView(views.APIView):
    authentication_classes = []  # Disables authentication
    permission_classes = []  # Disables permission

    def patch(self, request, token, message_id, *args, **kwargs):
        # Retrieve the new status from the request data
        new_status = request.data.get('status')
        valid_statuses = [BYOCMessageStates.PENDING, BYOCMessageStates.PROCESSING,
                          BYOCMessageStates.COMPLETED, BYOCMessageStates.ABORTED,
                          BYOCMessageStates.ERROR]

        # Check if the new status is valid and allowed to be set
        if new_status not in valid_statuses:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPDATE_MSG_STATUS.value,
                DNTag.DNMsg.value: "Invalid status provided:" + str(new_status),
            })

            return Response(
                {"detail": "Invalid status provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the message state object
        message_state = get_object_or_404(
            BYOCMessageState,
            id=message_id,
            token=token
        )

        print("ATTEMPTING STATUS PATCH FROM: " + str(message_state.status) + " TO: " + str(new_status))
        # Check if the status transition is valid, here assuming you can only go from 'pending' to 'processing'
        if message_state.status == BYOCMessageStates.PENDING and new_status in valid_statuses:
            message_state.status = new_status
            message_state.save(update_fields=['status'])

            dn_tracer.log_event(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPDATE_MSG_STATUS.value,
                DNTag.DNMsg.value: 'updated to status to: ' + str(new_status),
            })

            return Response({'status': 'updated to' + str(new_status)}, status=status.HTTP_200_OK)
        else:
            dn_tracer.log_error(str(token), {
                DNTag.DNMsgStage.value: DNMsgStage.UPDATE_MSG_STATUS.value,
                DNTag.DNMsg.value: "Invalid status update request. msg_id: " + str(message_id) + " status: " + str(message_state.status),
            })
            # Respond with a conflict status if the message is not in 'pending' state or transition is not allowed
            return Response(
                {"detail": "Invalid status update request."},
                status=status.HTTP_409_CONFLICT
            )
