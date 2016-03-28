from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .forms import InvitationForm, AddGuestForm, UpdateGuestForm
from django.forms import modelformset_factory
from django.core.urlresolvers import reverse
from .models import Invitation, Guest
from django.db.models import Count
from django.contrib import messages
import string

@login_required
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    form = InvitationForm()
    invitations = Invitation.objects.all().order_by("name").annotate(Count('guest'))
    guests = Guest.objects.all()

    lizts = (
        invitations,
        guests
    )

    total = (
        "Total",
        invitations.count(),
        guests.count(),
    )
    gupta = (
        "Gupta Family",
        invitations.filter(invited_by="gupta").count(),
        guests.filter(invitation__invited_by="gupta").count(),
    )
    verma = (
        "Verma Family",
        invitations.filter(invited_by="verma").count(),
        guests.filter(invitation__invited_by="verma").count(),
    )

    stats = (gupta, verma, total)

    context = {
        "form": form,
        "stats": stats,
        "lizts": lizts,
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
            messages.success(
                request,
                "Added {}".format(form.cleaned_data["name"])
            )
        else:
            messages.error(
                request,
                "Uh oh...somethings not right"
            )
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
                password=invitation.password())
            invitation.user = user
            invitation.save()
            messages.success(
                request,
                "created {} invitation".format(form.cleaned_data["name"])
            )
        else:
            messages.error(
                request,
                "sorry that is not a valid invitation"
            )
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
            messages.success(
                request,
                "saved {}'s rsvp".format(guest.name)
            )
        else:
            messages.error(
                request,
                "something's not right"
            )
    return redirect(invitation)
