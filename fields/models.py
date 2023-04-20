from django.db import models
from cities_light.models import City
from users.models import User

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
    type=models.ForeignKey(FieldType, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    SOIL_TYPES = (('synthetique', 'Synthetique'),
                  ('naturelle', 'Naturelle'))
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='football-fields',null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


