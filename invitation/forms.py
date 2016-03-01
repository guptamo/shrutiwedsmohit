from django.forms import ModelForm
from .models import Guest, Invitation


class InvitationForm(ModelForm):

    class Meta:
        model = Invitation
        fields = [
            "name",
            "invited_by",
            "invited_sangeet",
            "invited_ceremony",
            "invited_reception"]

class GuestForm(ModelForm):

    class Meta:
        model = Guest
        fields = [
            "name",
            "attending_sangeet",
            "attending_ceremony",
            "attending_reception",
            "meal_choice",
            "note"]
