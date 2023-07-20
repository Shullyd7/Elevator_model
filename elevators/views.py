from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Elevator
from .serializers import ElevatorSerializer, ElevatorRequestSerializer


# Create your views here.

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    # API to initialize the elevator system with 'n' elevators
    def create(self, request, *args, **kwargs):
        num_elevators = request.data.get('num_elevators', 1)
        elevator_ids = []  # List to store the IDs of created elevators

        for _ in range(num_elevators):
            elevator = Elevator.objects.create()
            elevator_ids.append(elevator.id)

        return Response({'detail': f'{num_elevators} elevators created successfully.', 'elevator_ids': elevator_ids},
                        status=status.HTTP_201_CREATED)

    # API to fetch all requests for a given elevator
    def get_requests(self, request, pk=None):
        elevator = self.get_object()
        requests = elevator.requests.all()
        serializer = ElevatorRequestSerializer(requests, many=True)
        return Response(serializer.data)

    # API to fetch the next destination floor for a given elevator
    def get_next_destination_floor(self, request, pk=None):
        elevator = self.get_object()
        next_destination = elevator.get_next_destination()
        return Response({'next_destination': next_destination})

    # API to fetch if the elevator is moving up or down currently
    def is_moving_up_down(self, request, pk=None):
        elevator = self.get_object()
        is_moving_up = elevator.is_moving_up()
        is_moving_down = elevator.is_moving_down()
        return Response({'is_moving_up': is_moving_up, 'is_moving_down': is_moving_down})

    # API to save a user request to the list of requests for an elevator
    def save_user_request(self, request, pk=None):
        floor = request.data.get('floor')
        elevator_id = int(pk)  # Convert the pk to an integer

        # Check if the requested elevator ID is within the range of initialized elevators
        if not (1 <= elevator_id <= Elevator.objects.count()):
            return Response({'detail': f'Elevator with ID {elevator_id} does not exist.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Find the optimal elevator based on user request
        elevators = Elevator.objects.filter(is_operational=True)
        optimal_elevator = None
        min_distance = float('inf')

        for elevator in elevators:
            distance = elevator.distance_from_floor(floor)
            if distance < min_distance:
                min_distance = distance
                optimal_elevator = elevator

        if optimal_elevator:
            optimal_elevator.add_request(floor)
            optimal_elevator.save()  # Save the updated elevator status to the database
            return Response({'detail': f'Request added to elevator {optimal_elevator.id}.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'No operational elevator available at the moment.'},
                            status=status.HTTP_400_BAD_REQUEST)

    # API to clear user requests
    def clear_user_requests(self, request, pk=None):
        elevator = self.get_object()
        elevator.requests.all().delete()
        elevator.save()
        return Response({'detail': f'All requests cleared from elevator {pk}.'},
                        status=status.HTTP_200_OK)

    # API to mark an elevator as not working or in maintenance
    def mark_maintenance(self, request, pk=None):
        elevator = self.get_object()
        elevator.is_operational = False
        elevator.save()
        return Response({'detail': f'Elevator {pk} marked as not working.'}, status=status.HTTP_200_OK)

    # API to open the door
    def open_door(self, request, pk=None):
        elevator = self.get_object()
        elevator.is_door_open = True
        elevator.save()
        return Response({'detail': f'Door of elevator {pk} opened.'}, status=status.HTTP_200_OK)

    # API to close the door
    def close_door(self, request, pk=None):
        elevator = self.get_object()
        elevator.is_door_open = False
        elevator.save()
        return Response({'detail': f'Door of elevator {pk} closed.'}, status=status.HTTP_200_OK)
