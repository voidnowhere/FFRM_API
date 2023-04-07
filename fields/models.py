from django.db import models


class Type(models.Model):

    TYPE_CHOICES = (
        ('7x7', '5x5'),
        ('7vs7', '5vs5')
    )
    name = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255,)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(max_length=255,)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE, related_name='fields')
    url_photo = models.URLField()
    TYPE_CHOICES2 = (('synthetique', 'Synthetique'),
                     ('naturelle', 'Naturelle'))
    soil_type = models.CharField(max_length=20, choices=TYPE_CHOICES2)

   

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

