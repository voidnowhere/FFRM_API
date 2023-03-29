from django.db import models

# Create your models here.
class Players(models.Model):
    name = models.CharField(max_length=100)


class Reservations(models.Model):
    beginHour = models.DateTimeField()
    endHour = models.DateTimeField()
    isPaid = models.BooleanField(default=False)
    player = models.ForeignKey(Players , on_delete=models.CASCADE)
