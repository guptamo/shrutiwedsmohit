from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import InvitationForm
from django.core.urlresolvers import reverse
import string


def password_generator(name):
    """
    Utility function which generates a password based on the given name. based
    off a super basic caesar cypher.
    """
    letters = [letter for letter in string.ascii_lowercase]
    letters_to_numbers = dict(zip(letters, range(26)))

    raw_password = ""
    for character in name:
        if character.isalpha():
            raw_password += str(letters_to_numbers[character.lower()])
        else:
            raw_password += str(character)

    password = raw_password[-6:]
    return password


@login_required
def dashboard(request, form=None):
    if form == None:
        form = InvitationForm()
    return render(request, "invitation/dashboard.html", context={"form": form})

@login_required
def invitation(request, invitation_name):
    return render(request, "invitation/invitation.html")

@login_required
def add_invitation(request):
    if request.method == "POST":
        form = InvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save()
            user = User.objects.create_user(
                username=form.cleaned_data["name"],
                password=password_generator(form.cleaned_data["name"]))
            invitation.user = user
            invitation.save()
        else:
            context = {"form": form}
            render(request, "invitation/dashboard.html", context)
    return redirect(reverse("invitation:dashboard"))
