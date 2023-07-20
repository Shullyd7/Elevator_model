from rest_framework import serializers
from .models import Elevator, ElevatorRequest

class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElevatorRequest
        fields = '__all__'

class ElevatorSerializer(serializers.ModelSerializer):
    requests = ElevatorRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Elevator
        fields = '__all__'
