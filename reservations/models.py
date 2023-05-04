from django.db import models

from fields.models import Field
from users.models import User


class Reservation(models.Model):
    begin_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    is_public = models.BooleanField(default=False)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    field = models.ForeignKey(Field, on_delete=models.PROTECT)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reservations')
    players = models.ManyToManyField(User, related_name='reservations_players')

    def __str__(self):
        return f'{self.field} {self.field.type} {self.begin_date_time} {self.end_date_time}'
