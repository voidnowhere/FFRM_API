from django.db import models


# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)


class TypeField(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()


class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(TypeField, on_delete=models.PROTECT)


class Reservation(models.Model):
    begin_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_public = models.BooleanField(default='False')
    players = models.ManyToManyField(Player, related_name='players')
    price = models.FloatField()
    owner = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='owner')
    field = models.ForeignKey(Field, on_delete=models.PROTECT)
