from django.forms import ModelForm, Textarea
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

        label_suffix = {field: "" for field in fields}



class AddGuestForm(ModelForm):

    class Meta:
        model = Guest
        fields =["name"]

        label_suffix = {field: "" for field in fields}


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
                "placeholder": "Food Allergies? Are you a child? Anything else we need to know?",
            })
        }
        
        label_suffix = {field: "" for field in fields}
