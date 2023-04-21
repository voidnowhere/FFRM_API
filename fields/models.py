from django.db import models
from users.models import User
from zones.models import Zone
from field_types.models import FootBallFieldType


class Field(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255,)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(max_length=255,)
    type=models.ForeignKey(FootBallFieldType, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    SOIL_TYPES = (('synthetique', 'Synthetique'),
                  ('naturelle', 'Naturelle'))
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='football-fields',null=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


