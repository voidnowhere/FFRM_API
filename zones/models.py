from django.db import models
from cities.models import City

class Zone(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.name