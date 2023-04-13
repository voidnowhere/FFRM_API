from django.db import models
from cities_light.models import City


class Zone(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class FieldType(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
class Field(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255,)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(max_length=255,)
    field_type=models.ForeignKey(FieldType, on_delete=models.PROTECT)
    state = models.BooleanField(default=False)
    SOIL_TYPES = (('synthetique', 'Synthetique'),
                  ('naturelle', 'Naturelle'))
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


