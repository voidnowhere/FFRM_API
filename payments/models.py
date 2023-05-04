from django.db import models

from reservations.models import Reservation


class Payment(models.Model):
    pid = models.CharField(max_length=255)
    created = models.DateTimeField()
    reservation = models.OneToOneField(Reservation, on_delete=models.PROTECT, related_name='payment')

    def __str__(self):
        return f'{self.id} {self.created}'
