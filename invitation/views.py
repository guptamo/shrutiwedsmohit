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
    raw_password = \
        "".join([str(letters_to_numbers[character]) for character in name])
    length = len(raw_password)
    password = raw_password[length-6:length]
    return password


@login_required
def dashboard(request, form=None):
    if form=None:
        form = InvitationForm()
    return render(request, "invitation/dashboard.html", {"form": form})

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
    return redirect(reverse("invitation:dashboard"))
