from django.db import models

from users.models import User


class FootBallFieldType(models.Model):
    name = models.CharField(max_length=100)
    max = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name}'


class FootBallField(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FootBallFieldType, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.type}'


class Reservation(models.Model):
    begin_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    field = models.ForeignKey(FootBallField, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owner')
    players = models.ManyToManyField(User, related_name='players')

    def __str__(self):
        return f'{self.field} {self.begin_date_time} {self.end_date_time}'
