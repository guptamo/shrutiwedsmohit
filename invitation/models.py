from django.db import models
from django.contrib.auth.models import User as Invitation


# Create your models here.
class Guest(models.Model):
    VERMA = "verma"
    GUPTA = "gupta"
    VEG = "veg"
    NON_VEG = "non-veg"

    INVITED_BY_CHOICES = (
        (VERMA, "Verma Family"),
        (GUPTA, "Gupta Family"),)

    MEAL_CHOICES = (
        (VEG, "Vegetarian"),
        (NON_VEG, "Non-vegetarian"),)

    name = models.CharField(max_length=40)
    invitation = models.ForeignKey(Invitation, null=True, blank=True)
    invited_by = models.CharField(max_length=5, choices=INVITED_BY_CHOICES)
    invited_sangeet = models.BooleanField(default=False)
    invited_ceremony = models.BooleanField(default=False)
    invited_reception = models.BooleanField(default=False)
    attending_sangeet = models.BooleanField(default=False)
    attending_ceremony = models.BooleanField(default=False)
    attending_reception = models.BooleanField(default=False)
    meal_choice = models.CharField(max_length=7, choices=MEAL_CHOICES)
    note = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'

    def __str__(self):
        return self.name
