from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import string


class Invitation(models.Model):
    VERMA = "verma"
    GUPTA = "gupta"

    INVITED_BY_CHOICES = (
        (None, "Invited By"),
        (VERMA, "Verma Family"),
        (GUPTA, "Gupta Family"),
    )

    user = models.OneToOneField(User, null=True, blank=True)
    name = models.SlugField(max_length=20, unique=True)
    invited_by = models.CharField(max_length=5, choices=INVITED_BY_CHOICES)

    invited_sangeet = models.BooleanField(default=False)
    invited_ceremony = models.BooleanField(default=False)
    invited_reception = models.BooleanField(default=False)
    rsvp = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("invitation:invitation", args=[self.name])

    def guest_list(self):
        guests = self.guest_set.all()
        guest_list = ""
        for guest in guests:
            guest_list += "{}<br>".format(guest.name)
        return guest_list

    def password(self):
        """
        Utility function which generates a password based on the given name. based
        off a super basic caesar cypher.
        """
        letters = [letter for letter in string.ascii_lowercase]
        letters_to_numbers = dict(zip(letters, range(26)))

        raw_password = ""
        for character in self.name:
            if character.isalpha():
                raw_password += str(letters_to_numbers[character.lower()])
            elif character == "_" or character == "-":
                raw_password += str(character)
            else:
                raw_password += str(character)

        return raw_password[-6:]

# Create your models here.
class Guest(models.Model):
    VEG = "veg"
    NON_VEG = "non-veg"

    MEAL_CHOICES = (
        (None, "Reception Meal Choice"),
        (VEG, "Vegetarian"),
        (NON_VEG, "Non-vegetarian (Fish and Chicken)"),
    )

    name = models.CharField(max_length=40)
    invitation = models.ForeignKey(Invitation, null=True, blank=True)
    attending_sangeet = models.BooleanField(default=False)
    attending_ceremony = models.BooleanField(default=False)
    attending_reception = models.BooleanField(default=False)
    meal_choice = models.CharField(max_length=7, choices=MEAL_CHOICES, blank=True)
    note = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'Guest'
        verbose_name_plural = 'Guests'
        unique_together = ("name", "invitation")

    def __str__(self):
        return self.name
