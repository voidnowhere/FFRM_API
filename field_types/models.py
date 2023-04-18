from django.db import models

from users.models import User


# Create your models here.
class FootBallField(models.Model):
    name = models.CharField(max_length=10)


class FootBallFieldType(models.Model):
    name = models.CharField(max_length=10)
    max = models.IntegerField()
    priceHour = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
