from django.db import models



class Terrain(models.Model):
    nom = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    laltitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()

    #TYPE_CHOICES = (('7x7', '5x5'),('7vs7', '5vs5'))
    #TYPE_CHOICES2 = (('synthetique', 'naturelle'),('Synthetique', 'Naturelle'))
    type = models.ForeignKey('Type', on_delete=models.CASCADE)

    etat = models.BooleanField(default=False)
    price = models.FloatField()
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    url_photo = models.URLField()

    type_sole = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('City', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

