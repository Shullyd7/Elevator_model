from django.shortcuts import render
from rest_framework import viewsets
from .models import Elevator
from .serializers import ElevatorSerializer
# Create your views here.

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer
