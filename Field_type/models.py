from django.db import models

# Create your models here.
class FootBallField(models.Model):
    name = models.CharField(max_length=10)

class FootBallFieldType(models.Model):
    footBallField = models.ForeignKey(FootBallField, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    max = models.IntegerField()
    price = models.FloatField()
    advance = models.FloatField()