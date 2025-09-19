from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class CropPredictionForm(forms.Form):
    nitrogen = forms.FloatField(label='Nitrogen', validators=[MinValueValidator(0), MaxValueValidator(140)])
    phosphorus = forms.FloatField(label='Phosphorus', validators=[MinValueValidator(5), MaxValueValidator(145)])
    potassium = forms.FloatField(label='Potassium', validators=[MinValueValidator(5), MaxValueValidator(205)])
    temperature = forms.FloatField(label='Temperature', validators=[MinValueValidator(7), MaxValueValidator(45)])
    humidity = forms.FloatField(label='Humidity', validators=[MinValueValidator(13), MaxValueValidator(100)])
    ph = forms.FloatField(label='pH', validators=[MinValueValidator(3), MaxValueValidator(14)])
    rainfall = forms.FloatField(label='Rainfall', validators=[MinValueValidator(20), MaxValueValidator(500)])
 