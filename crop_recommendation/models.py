# models.py
from django.db import models
from django.contrib.auth.models import User

class CropPrediction(models.Model):
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    predicted_crop = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.timestamp} - {self.predicted_crop}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    land = models.ForeignKey(CropPrediction, on_delete=models.CASCADE,null = True, blank=True)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username