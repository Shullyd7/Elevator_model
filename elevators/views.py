from django.db import connection
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Elevator, ElevatorRequest
from .serializers import ElevatorSerializer, ElevatorRequestSerializer


# Create your views here.

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    # API to initialize the elevator system with 'n' elevators
    def create(self, request, *args, **kwargs):
        num_elevators = request.data.get('num_elevators', 1)
        for _ in range(num_elevators):
            Elevator.objects.create()
        return Response({'detail': f'{num_elevators} elevators created successfully.'}, status=status.HTTP_201_CREATED)

    # API to fetch the number of elevators in the system
    def get_num_elevators(self, request):
        elevators = self.queryset
        num_elevators = elevators.count()
        elevator_ids = [elevator.id for elevator in elevators]
        return Response({'num_elevators': num_elevators, 'elevator_ids': elevator_ids}, status=status.HTTP_200_OK)

    # API to clear all initialized elevators from the system
    def clear_elevators(self, request):
        # Delete all associated ElevatorRequest objects first
        ElevatorRequest.objects.all().delete()

        # Clear all elevators from the database
        self.queryset.delete()

        # Manually reset the primary key sequence for Elevator model
        table_name = Elevator._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM SQLITE_SEQUENCE WHERE NAME='{table_name}'")
            cursor.execute(f"INSERT INTO SQLITE_SEQUENCE (NAME, SEQ) VALUES ('{table_name}', 0)")

        return Response({'detail': 'All initialized elevators have been cleared.'}, status=status.HTTP_200_OK)

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

        # Find the optimal elevator based on user request
        elevators = Elevator.objects.filter(is_operational=True)
        optimal_elevator = None
        min_distance = float('inf')

        for elevator in elevators:
            distance = elevator.distance_from_floor(floor)
            if elevator.is_moving_up() and floor >= elevator.floor:
                if distance < min_distance:
                    min_distance = distance
                    optimal_elevator = elevator
            elif elevator.is_moving_down() and floor <= elevator.floor:
                if distance < min_distance:
                    min_distance = distance
                    optimal_elevator = elevator
            elif not elevator.is_moving:
                if distance < min_distance:
                    min_distance = distance
                    optimal_elevator = elevator

        if optimal_elevator:
            optimal_elevator.add_request(floor)
            optimal_elevator.save()  # Save the updated elevator status to the database
            return Response({'detail': f'Request added to elevator {optimal_elevator.id}.'}, status=status.HTTP_200_OK)
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