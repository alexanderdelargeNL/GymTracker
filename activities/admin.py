# activities/admin.py
from django.contrib import admin
from .models import MuscleGroup, Activity, CardioExercise, Location

admin.site.register(MuscleGroup)
admin.site.register(CardioExercise)
admin.site.register(Activity)
admin.site.register(Location)