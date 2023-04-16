from django.db import models

from users.models import User


class FieldType(models.Model):
    name = models.CharField(max_length=100)
    max_players = models.PositiveSmallIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.name}'


class Field(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(FieldType, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.type}'


class Payment(models.Model):
    pid = models.CharField(max_length=40)
    created = models.DateTimeField()

    def __str__(self):
        return f'{self.pid} {self.created}'


class Reservation(models.Model):
    begin_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    field = models.ForeignKey(Field, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='owner')
    players = models.ManyToManyField(User, related_name='players')
    payment = models.OneToOneField(Payment, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'{self.field} {self.begin_date_time} {self.end_date_time}'
