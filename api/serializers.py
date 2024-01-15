# BYO_COMPUTE_API
from rest_framework import serializers


from byo_network_hub.models import ConnectionStatus, ComputeContract, BYOCMessageState

class ConnectionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionStatus
        fields = '__all__'


from rest_framework import serializers
from byo_network_hub.models import ComputeContract

class ComputeContractSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = ComputeContract
        fields = '__all__'

    def create(self, validated_data):
        # Check if an instance with the provided id exists
        contract_id = validated_data.get('id')
        if contract_id:
            instance, created = ComputeContract.objects.get_or_create(
                id=contract_id,
                defaults=validated_data
            )
            if not created:
                # Update instance if it already exists
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
            return instance
        else:
            # Create a new instance if no id is provided
            return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



class BYOCMessageStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BYOCMessageState
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
