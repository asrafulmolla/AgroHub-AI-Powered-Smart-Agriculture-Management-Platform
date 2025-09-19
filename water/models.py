from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)
    base_interval_days = models.IntegerField()  
    base_water_litre = models.FloatField()      
    icon = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name
