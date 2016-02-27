from django.forms import ModelForm
from .models import Guest

class GuestForm(ModelForm):

    class Meta:
        model = Guest
        fields = [
            "name",
            "invited_by",
            "invited_sangeet",
            "invited_ceremony",
            "invited_reception",
            "attending_sangeet",
            "attending_ceremony",
            "attending_reception",
            "meal_choice",
            "note"]
