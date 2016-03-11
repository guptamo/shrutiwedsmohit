from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import InvitationForm, AddGuestForm, UpdateGuestForm
from django.forms import modelformset_factory
from django.core.urlresolvers import reverse
from .models import Invitation, Guest
import string

def invitation_access_check(request, invitation_name):
    """
    Utility function to determine whether or not the guest has access to this
    invitation or invitation function. Stop gap until I write out a decorator
    """
    return request.user.invitation.name == invitation_name

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
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    form = InvitationForm()
    invitations = Invitation.objects.all().order_by("name")
    passwords = \
        [password_generator(invitation.name) for invitation in invitations]
    invite_info = tuple(zip(invitations, passwords))
    context = {
        "form": form,
        "invite_info": invite_info
    }
    return render(request, "invitation/dashboard.html", context)

@login_required
def invitation(request, invitation_name):
    # if not invitation_access_check(request, invitation_name):
    #     return redirect(request.user.invitation.get_absolute_url())
    invitation = get_object_or_404(Invitation, name=invitation_name)
    guests = invitation.guest_set.all().order_by("name")
    guest_forms = []
    for guest in guests:
        guest_forms.append(UpdateGuestForm(instance=guest))
    guest_list = zip(guests, guest_forms)
    add_guest_form = AddGuestForm()
    context = {
        "invitation": invitation,
        "guest_list": guest_list,
        "add_guest_form": add_guest_form,
    }
    return render(request, "invitation/invitation.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_guest(request, invitation_name):
    if request.method == "POST":
        invitation = get_object_or_404(Invitation, name=invitation_name)
        form = AddGuestForm(request.POST)
        if form.is_valid():
            guest = form.save()
            guest.invitation = invitation
            guest.save()
    return redirect(invitation)

@login_required
@user_passes_test(lambda u: u.is_staff)
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
    return redirect(reverse("invitation:dashboard"))

@login_required
def update_guest(request, invitation_name, guest_pk):
    # if not invitation_access_check(request, invitation_name):
    #     return redirect(request.user.invitation.get_absolute_url())
    guest = get_object_or_404(Guest, pk=guest_pk)
    invitation = get_object_or_404(Invitation, name=invitation_name)
    if request.method == "POST":
        form = UpdateGuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
    return redirect(invitation)
