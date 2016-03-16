from django.forms import ModelForm, BaseModelFormSet, Textarea
from .models import Guest, Invitation


class InvitationForm(ModelForm):

    class Meta:
        model = Invitation
        fields = [
            "name",
            "invited_by",
            "invited_sangeet",
            "invited_ceremony",
            "invited_reception"
        ]


class AddGuestForm(ModelForm):

    class Meta:
        model = Guest
        fields =["name"]

class UpdateGuestForm(ModelForm):

    class Meta:
        model = Guest
        fields = [
            "attending_sangeet",
            "attending_ceremony",
            "attending_reception",
            "meal_choice",
            "note"
        ]
        widgets = {
            "note": Textarea(attrs={
                "class": "materialize-textarea",
            })
        }
