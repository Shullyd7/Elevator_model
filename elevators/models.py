from django.db import models


class Elevator(models.Model):
    floor = models.PositiveIntegerField(default=1)
    direction = models.CharField(max_length=5, choices=[('UP', 'Up'), ('DOWN', 'Down'), ('STOP', 'Stop')], default='STOP')
    is_moving = models.BooleanField(default=False)
    is_operational = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=False)

    def __str__(self):
        return f"Elevator {self.id}"

    def get_next_destination(self):
        if self.is_moving:
            if self.direction == 'UP':
                requests_above = self.requests.filter(floor__gt=self.floor).order_by('floor')
                return requests_above.first().floor if requests_above.exists() else None
            elif self.direction == 'DOWN':
                requests_below = self.requests.filter(floor__lt=self.floor).order_by('-floor')
                return requests_below.first().floor if requests_below.exists() else None
        return None

    @property
    def next_floor(self):
        if self.requests.exists():
            return self.requests.first().floor
        return None

    def is_moving_up(self):
        return self.is_moving and self.direction == 'UP'

    def is_moving_down(self):
        return self.is_moving and self.direction == 'DOWN'

    def add_request(self, floor):
        ElevatorRequest.objects.create(elevator=self, floor=floor)

        # Handle the movement of the elevator
        if self.is_moving:
            next_destination = self.get_next_destination()
            if next_destination is not None:
                if next_destination > self.floor:
                    self.direction = 'UP'
                elif next_destination < self.floor:
                    self.direction = 'DOWN'
            else:
                self.direction = 'STOP'
        else:
            self.is_moving = True
            next_destination = self.get_next_destination()
            if next_destination is not None:
                if next_destination > self.floor:
                    self.direction = 'UP'
                elif next_destination < self.floor:
                    self.direction = 'DOWN'
            else:
                self.direction = 'STOP'

    def distance_from_floor(self, floor):
        return abs(self.floor - floor)


class ElevatorRequest(models.Model):
    elevator = models.ForeignKey(Elevator, related_name='requests', on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()

    def __str__(self):
        return f"Request {self.id} for Elevator {self.elevator.id}"


