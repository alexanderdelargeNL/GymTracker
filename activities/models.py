# activities/models/py
from django.db import models

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CardioExercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    date = models.DateField()
    duration = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)
    musclegroup = models.ForeignKey(MuscleGroup, null=True, blank=True, on_delete=models.SET_NULL)
    cardioexercise = models.ForeignKey(CardioExercise, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    is_rest = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.date} - {self.musclegroup} - {self.cardioexercise} - {self.duration} min"



