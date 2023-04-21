from django.db import models

from users.models import User


class FieldType(models.Model):
    name = models.CharField(max_length=10)
    max_players = models.PositiveSmallIntegerField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}'
