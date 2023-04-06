from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)

class Field(models.Model):
    name = models.CharField(max_length=100)
class Reservation(models.Model):
    begin_date_time  = models.DateTimeField()
    end_date_time  = models.DateTimeField()
    isPaid = models.BooleanField(default=False)
    player = models.ManyToManyField(Player, related_name='reservations')
    field = models.ForeignKey(Field, on_delete= models.CASCADE)

