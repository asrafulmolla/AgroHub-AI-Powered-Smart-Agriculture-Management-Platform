from django.urls import path
from . import views

urlpatterns = [
    path("irrigation/", views.irrigation_schedule, name="irrigation"),
]