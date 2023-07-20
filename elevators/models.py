from django.db import models

# Create your models here.

class Elevator(models.Model):
    floor = models.PositiveIntegerField(default=1)
    direction = models.CharField(max_length=5, choices=[('UP', 'Up'), ('DOWN', 'Down'), ('STOP', 'Stop')], default='STOP')
    is_moving = models.BooleanField(default=False)
    is_operational = models.BooleanField(default=True)

    def __str__(self):
        return f"Elevator {self.id}"
